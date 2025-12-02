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

class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('login')

    def get_logged_in_traveler(self):
        if not self.request.user.is_authenticated:
            return None
        return Traveler.objects.filter(user = self.request.user).first()


def homepage(request):
    return render(request,'project/homepage.html')

class UserRegistrationView(CreateView):
    template_name = 'project/signup.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        return reverse('login')

class TravelerListView(ListView):
    model = Traveler 
    template_name = "project/show_all_travelers.html"
    context_object_name = "travelers"

class TravelerDetailView(DetailView):
    model = Traveler 
    template_name = "project/show_traveler.html"
    context_object_name = "traveler"

class TravelerCreateView(CreateView):
    model = Traveler
    form_class = CreateTravelerForm
    template_name = "project/create_traveler_form.html"

    def get_success_url(self):
        return reverse('travelers')

class TravelerUpdateView(UpdateView):
    model = Traveler
    form_class = UpdateTravelerForm
    template_name = "project/update_traveler_form.html"


class TravelerDeleteView(DeleteView):
    model = Traveler
    template_name = "project/delete_traveler_form.html"
    def get_success_url(self):
        return reverse('travelers')


# ---------------------------------



class TripListView(MyLoginRequiredMixin, ListView):
    model = Trip
    template_name= "project/show_all_trips.html"
    context_object_name = "trips"

    def get_queryset(self):
        """
        Annotate each trip with how many itinerary stops it currently has so the
        template can render the count without extra queries.
        """
        queryset = Trip.objects.select_related("traveler").annotate(
            num_stops=Count("itinerarystop")
        )
        if self.request.user.is_authenticated:
            return queryset.filter(traveler__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_stop_counts"] = {
            trip.pk: trip.num_stops for trip in context["trips"]
        }
        traveler = self.get_logged_in_traveler()
        context["traveler"] = traveler.full_name if traveler else ""
        return context
    
class TripDetailView(MyLoginRequiredMixin, DetailView):
    model = Trip 
    template_name= "project/show_trip.html"
    context_object_name= "trip"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["subtrips"] = self.object.sub_trips.all()
        context["stops"] = (
            ItineraryStop.objects.filter(trip=self.object)
            .select_related("trip") #SQL join
            .prefetch_related("booking_set") #query all bookings
            .order_by("orderIndex", "date")
        )
        context["bookings"] = Booking.objects.filter(stop__trip=self.object).select_related(
            "stop", "stop__trip" #join both stop and stop__trip instead of making 2 queries
        )
        return context

class TripCreateView(MyLoginRequiredMixin, CreateView):
    form_class = CreateTripForm
    template_name = "project/create_trip_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.parent_trip = None
        parent_pk = self.kwargs.get("parent_pk")
        if parent_pk is not None:
            traveler = self.get_logged_in_traveler()
            if traveler:
                self.parent_trip = Trip.objects.filter(
                    pk=parent_pk, traveler=traveler
                ).first()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_trip"] = self.parent_trip
        return context

    def form_valid(self, form):
        form.instance.traveler = self.get_logged_in_traveler()
        if self.parent_trip:
            form.instance.parent_trip = self.parent_trip
        return super().form_valid(form)


class TripUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Trip
    form_class = UpdateTripForm
    template_name = "project/update_trip_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_trip"] = self.object.parent_trip
        return context

    def form_valid(self, form):
        form.instance.traveler = self.get_logged_in_traveler()
        return super().form_valid(form)

class TripDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Trip 
    template_name="project/delete_trip_form.html"

    def get_success_url(self):
        return reverse('triplist')



# ---------------------------------



class ItineraryStopListView(ListView):
    model = ItineraryStop
    template_name="project/show_all_itinerarystops.html"
    context_object_name = "stops"


class ItineraryStopDetailView(DetailView):
    model = ItineraryStop
    template_name="project/show_itinerarystop.html"
    context_object_name = "stop"


class ItineraryStopCreateView(MyLoginRequiredMixin, CreateView):
    model = ItineraryStop
    form_class = CreateItineraryStopForm
    template_name = "project/create_itinerarystop_form.html"

    def dispatch(self, request, *args, **kwargs):
        trip_pk = self.kwargs["trip_pk"]
        self.trip = Trip.objects.get(pk=trip_pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.trip = self.trip
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.trip
        return context

    def get_success_url(self):
        return self.trip.get_absolute_url()


class ItineraryStopUpdateView(MyLoginRequiredMixin, UpdateView):
    model = ItineraryStop
    form_class = UpdateItineraryStopForm
    template_name = "project/update_itinerarystop_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.object.trip
        return context

    def get_success_url(self):
        return self.object.trip.get_absolute_url()


class ItineraryStopDeleteView(MyLoginRequiredMixin, DeleteView):
    model = ItineraryStop
    template_name = "project/delete_itinerarystop_form.html"

    def get_success_url(self):
        return self.object.trip.get_absolute_url()



# ---------------------------------



class BookingListView(ListView):
    model = Booking
    template_name = "project/show_all_bookings.html"
    context_object_name = "bookings"


class BookingDetailView(DetailView):
    model = Booking
    template_name = "project/show_booking.html"
    context_object_name = "booking"


class BookingCreateView(MyLoginRequiredMixin, CreateView):
    model = Booking
    form_class = CreateBookingForm
    template_name = "project/create_booking_form.html"

    def dispatch(self, request, *args, **kwargs):
        trip_pk = self.kwargs["trip_pk"]
        traveler = self.get_logged_in_traveler()
        if traveler is None:
            self.trip = None
        else:
            self.trip = Trip.objects.filter(pk=trip_pk, traveler=traveler).first()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        stop_field = form.fields.get("stop")
        if stop_field is not None:
            if self.trip:
                stop_field.queryset = self.trip.itinerarystop_set.all()
            else:
                stop_field.queryset = ItineraryStop.objects.none()
        return form

    def form_valid(self, form):
        stop = form.cleaned_data.get("stop")
        if not stop or stop.trip_id != (self.trip.pk if self.trip else None):
            form.add_error("stop", "Please choose a stop from this trip.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.trip
        context["stops"] = self.trip.itinerarystop_set.all() if self.trip else ItineraryStop.objects.none()
        return context

    def get_success_url(self):
        return self.trip.get_absolute_url() if self.trip else reverse("triplist")


class BookingUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Booking
    form_class = UpdateBookingForm
    template_name = "project/update_booking_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.object.stop.trip
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        trip = self.object.stop.trip
        stop_field = form.fields.get("stop")
        if stop_field is not None:
            stop_field.queryset = trip.itinerarystop_set.all()
        return form

    def form_valid(self, form):
        stop = form.cleaned_data.get("stop")
        if stop.trip != self.object.stop.trip:
            form.add_error("stop", "Please choose a stop from this trip.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.stop.trip.get_absolute_url()


class BookingDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Booking
    template_name = "project/delete_booking_form.html"

    def get_success_url(self):
        return self.object.stop.trip.get_absolute_url()
