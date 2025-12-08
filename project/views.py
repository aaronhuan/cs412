# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),11/22/2025
# Description: Class based views for Project pages, inherits from django generic views, django authentication, and mixins. 

from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Count
from .models import Traveler, Trip, ItineraryStop, Booking
from .forms import (
    CreateTravelerForm,
    UpdateTravelerForm,
    CreateTripForm,
    UpdateTripForm,
    CreateItineraryStopForm,
    UpdateItineraryStopForm,
    CreateBookingForm,
    UpdateBookingForm,
)
from django.contrib.auth import login 

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Class that inherits from built in LoginRequiredMixin, used to override or add methods."""
    def get_login_url(self):
        """Obtain the url that displays the login form."""
        return reverse('login')

    def get_logged_in_traveler(self):
        """Query for the profile associated with the logged in user."""
        if not self.request.user.is_authenticated:
            return None
        return Traveler.objects.filter(user = self.request.user).first()


def homepage(request):
    """Display the homepage template."""
    return render(request,'project/homepage.html')

# --------------------------------- Traveler Views 
class TravelerListView(ListView):
    """View to show all travelers. Currently only accessible by admin users for future features."""
    model = Traveler 
    template_name = "project/show_all_travelers.html"
    context_object_name = "travelers"

class TravelerDetailView(DetailView):
    """View to show a single traveler. Currently only accessible by admin users for future features."""
    model = Traveler 
    template_name = "project/show_traveler.html"
    context_object_name = "traveler"

class TravelerCreateView(CreateView):
    """View to create a new traveler profile along with a user account."""
    model = Traveler
    form_class = CreateTravelerForm
    template_name = "project/create_traveler_form.html"

    def get_context_data(self, **kwargs):
        """Add the user creation form to the context."""
        context= super().get_context_data(**kwargs)
        context['create_user_form']= UserCreationForm()
        return context
    
    def form_valid(self, form):
        """Create the user account and log in the new user upon successful profile creation."""
        user = UserCreationForm(self.request.POST).save()
        form.instance.user = user
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        """Upon successful creation, redirect to homepage."""
        return reverse('homepage')


class TravelerUpdateView(UpdateView):
    """View to update an existing traveler profile. Currently only accessible by admin users for future features."""
    model = Traveler
    form_class = UpdateTravelerForm
    template_name = "project/update_traveler_form.html"


class TravelerDeleteView(DeleteView):
    """View to delete an existing traveler profile. Currently only accessible by admin users for future features."""
    model = Traveler
    template_name = "project/delete_traveler_form.html"
    def get_success_url(self):
        return reverse('travelers')


# --------------------------------- Trip Views



class TripListView(MyLoginRequiredMixin, ListView):
    """View to show all trips for the logged in traveler."""
    model = Trip
    template_name= "project/show_all_trips.html"
    context_object_name = "trips"

    def get_queryset(self):
        """Obtain the queryset of trips for the logged in traveler."""
        
        """Use select_related (SQL Join) and annotate to count stops per Trip."""
        queryset = Trip.objects.select_related("traveler").annotate(
            num_stops=Count("itinerarystop")
        )
        if self.request.user.is_authenticated:
            return queryset.filter(traveler__user=self.request.user, parent_trip__isnull=True)
        return queryset.filter(parent_trip__isnull=True)

    def get_context_data(self, **kwargs):
        """Add number of stops per trip and traveler's full name to context."""
        context = super().get_context_data(**kwargs)
        context["trip_stop_counts"] = { # create a dict of trip pk to num stops (annotated earlier)
            trip.pk: trip.num_stops for trip in context["trips"]
        }
        traveler = self.get_logged_in_traveler()
        context["traveler"] = traveler.full_name if traveler else ""
        return context
    
class TripDetailView(MyLoginRequiredMixin, DetailView):
    """View to show details of a single trip, including its subtrips, itinerary stops, and bookings."""
    model = Trip 
    template_name= "project/show_trip.html"
    context_object_name= "trip"

    def get_context_data(self, **kwargs):
        """Add subtrips, itinerary stops, and bookings to context."""
        context= super().get_context_data(**kwargs)
        context["subtrips"] = self.object.sub_trips.all() 
        context["stops"] = ( #get all itinerary stops for this trip
            ItineraryStop.objects.filter(trip=self.object)
            .select_related("trip") #SQL join Trip and ItineraryStop
            .prefetch_related("booking_set") #seperate query all related bookings 
            .order_by("orderIndex", "date") # order by orderIndex then date
        )
        context["bookings"] = Booking.objects.filter(stop__trip=self.object).select_related(
            "stop", "stop__trip" #travel through foreign keys to join tables Trip, ItineraryStop, Booking
        )
        return context

class TripCreateView(MyLoginRequiredMixin, CreateView):
    """View to create a new trip or subtrip for the logged in traveler."""
    form_class = CreateTripForm
    template_name = "project/create_trip_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method operates before get/post to set parent trip if creating a subtrip."""
        self.parent_trip = None
        parent_pk = self.kwargs.get("parent_pk") # check if parent_pk is in url kwargs
        if parent_pk is not None: # creating a subtrip
            traveler = self.get_logged_in_traveler()
            if traveler:
                self.parent_trip = Trip.objects.filter( # ensure parent trip belongs to logged in traveler
                    pk=parent_pk, traveler=traveler
                ).first()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add parent trip to context if creating a subtrip else add None."""
        context = super().get_context_data(**kwargs)
        context["parent_trip"] = self.parent_trip
        return context

    def form_valid(self, form):
        """Assign the logged in traveler and parent trip (if any) to the new trip before saving."""
        form.instance.traveler = self.get_logged_in_traveler()
        if self.parent_trip:
            form.instance.parent_trip = self.parent_trip
        return super().form_valid(form)


class TripUpdateView(MyLoginRequiredMixin, UpdateView):
    """View to update an existing trip for the logged in traveler."""
    model = Trip
    form_class = UpdateTripForm
    template_name = "project/update_trip_form.html"

    def get_context_data(self, **kwargs):
        """Obtain parent trip to add to context."""
        context = super().get_context_data(**kwargs)
        context["parent_trip"] = self.object.parent_trip
        return context

    def form_valid(self, form):
        """Fill in the traveler as the logged in traveler before saving."""
        form.instance.traveler = self.get_logged_in_traveler()
        return super().form_valid(form)

class TripDeleteView(MyLoginRequiredMixin, DeleteView):
    """View to delete an existing trip for the logged in traveler."""
    model = Trip 
    template_name="project/delete_trip_form.html"

    def get_success_url(self):
        """After successful deletion, redirect to trip list."""
        return reverse('triplist')



# --------------------------------- Itinerary Stop Views



class ItineraryStopDetailView(MyLoginRequiredMixin,DetailView):
    """View to show details of a single itinerary stop."""
    model = ItineraryStop
    template_name="project/show_itinerarystop.html"
    context_object_name = "stop"


class ItineraryStopCreateView(MyLoginRequiredMixin, CreateView):
    """View to create a new itinerary stop for a specific trip."""
    model = ItineraryStop
    form_class = CreateItineraryStopForm
    template_name = "project/create_itinerarystop_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Get the trip for which the stop is being created before processing the request."""
        trip_pk = self.kwargs["trip_pk"]
        self.trip = Trip.objects.get(pk=trip_pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the trip to the new itinerary stop before saving."""
        form.instance.trip = self.trip
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add the parent trip of the stop to the context."""
        context = super().get_context_data(**kwargs)
        context["trip"] = self.trip
        return context

    def get_success_url(self):
        """Upon successful creation, redirect to the trip detail page."""
        return self.trip.get_absolute_url()


class ItineraryStopUpdateView(MyLoginRequiredMixin, UpdateView):
    """View to update an existing itinerary stop."""
    model = ItineraryStop
    form_class = UpdateItineraryStopForm
    template_name = "project/update_itinerarystop_form.html"

    def get_context_data(self, **kwargs):
        """Add the parent trip of the stop to the context."""
        context = super().get_context_data(**kwargs)
        context["trip"] = self.object.trip
        return context

    def get_success_url(self):
        """Upon successful update, redirect to the trip detail page."""
        return self.object.trip.get_absolute_url()


class ItineraryStopDeleteView(MyLoginRequiredMixin, DeleteView):
    """View to delete an existing itinerary stop."""
    model = ItineraryStop
    template_name = "project/delete_itinerarystop_form.html"

    def get_success_url(self):
        """Upon successful deletion, redirect to the trip detail page."""
        return self.object.trip.get_absolute_url()



# --------------------------------- Booking Views



class BookingDetailView(MyLoginRequiredMixin,DetailView):
    """View to show details of a single booking."""
    model = Booking
    template_name = "project/show_booking.html"
    context_object_name = "booking"


class BookingCreateView(MyLoginRequiredMixin, CreateView):
    """View to create a new booking for a specific trip."""
    model = Booking
    form_class = CreateBookingForm
    template_name = "project/create_booking_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Prior to processing the request, get the trip for which the booking is being created."""
        trip_pk = self.kwargs["trip_pk"]
        traveler = self.get_logged_in_traveler()
        if traveler is None:
            self.trip = None
        else:
            self.trip = Trip.objects.filter(pk=trip_pk, traveler=traveler).first()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """Limit the stop field for booking to stops belonging to the trip."""
        form = super().get_form(form_class)
        stop_field = form.fields.get("stop")
        if stop_field is not None:
            if self.trip:
                stop_field.queryset = self.trip.itinerarystop_set.all()
            else:
                stop_field.queryset = ItineraryStop.objects.none()
        return form

    def get_context_data(self, **kwargs):
        """Add the parent trip and stops to the context."""
        context = super().get_context_data(**kwargs)
        context["trip"] = self.trip
        context["stops"] = self.trip.itinerarystop_set.all() if self.trip else ItineraryStop.objects.none()
        return context

    def get_success_url(self):
        """Upon successful creation, redirect to the trip detail page."""
        return self.trip.get_absolute_url() if self.trip else reverse("triplist")


class BookingUpdateView(MyLoginRequiredMixin, UpdateView):
    """View to update an existing booking."""
    model = Booking
    form_class = UpdateBookingForm
    template_name = "project/update_booking_form.html"

    def get_context_data(self, **kwargs):
        """Get the trip associated with the booking's stop and add to context."""
        context = super().get_context_data(**kwargs)
        context["trip"] = self.object.stop.trip
        return context

    def get_form(self, form_class=None):
        """Limit the stop field for booking to stops belonging to the trip."""
        form = super().get_form(form_class)
        trip = self.object.stop.trip
        stop_field = form.fields.get("stop")
        if stop_field is not None:
            stop_field.queryset = trip.itinerarystop_set.all()
        return form

    def get_success_url(self):
        """Upon successful update, redirect to the trip detail page."""
        return self.object.stop.trip.get_absolute_url()


class BookingDeleteView(MyLoginRequiredMixin, DeleteView):
    """View to delete an existing booking."""
    model = Booking
    template_name = "project/delete_booking_form.html"

    def get_success_url(self):
        """Upon successful deletion, redirect to the trip detail page."""
        return self.object.stop.trip.get_absolute_url()
