from django.shortcuts import render
# Create your views here.
from .models import Traveler, Trip, ItineraryStop, Booking
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import CreateTripForm, UpdateTripForm


class TravelerListView(ListView):
    model = Traveler 
    template_name = "project/show_all_travelers.html"
    context_object_name = "travelers"

class TravelerDetailView(DetailView):
    model = Traveler 
    template_name = "project/show_traveler.html"
    context_object_name = "traveler"

# class TravelerCreateView(CreateView):
#     form_class = 
#     template_name =


# class TravelerUpdateView(UpdateView):
#     form_class = 
#     template_name =



# ---------------------------------



class TripListView(ListView):
    model = Trip
    template_name= "project/show_all_trips.html"
    context_object_name = "trips"

class TripDetailView(DetailView):
    model = Trip 
    template_name= "project/show_trip.html"
    context_object_name= "trip"

class TripCreateView(CreateView):
    form_class = CreateTripForm
    template_name = "project/create_trip_form.html"


class TripUpdateView(UpdateView):
    form_class = UpdateTripForm
    template_name = "project/update_trip_form.html"

class TripDeleteView(DeleteView):
    model = Trip 
    template_name="project/delete_trip_form.html"

    # def get_success_url(self):
    #     return self.object.



# ---------------------------------



class ItineraryStopListView(ListView):
    model = ItineraryStop
    template_name="project/show_all_itinerarystops.html"
    context_object_name = "stops"

class ItineraryStopDetailView(DetailView):
    model = ItineraryStop
    template_name="project/show_itinerarystop.html"
    context_object_name = "stop"

# class ItineraryStopCreateView(CreateView):
#     form_class = 
#     template_name =

# class ItineraryStopUpdateView(UpdateView):
#     form_class = 
#     template_name =



# ---------------------------------



class BookingListView(ListView):
    model = Booking
    template_name = "project/show_all_bookings.html"
    context_object_name = "bookings"

class BookingDetailView(DetailView):
    model = Booking
    template_name = "project/show_booking.html"
    context_object_name = "booking"


# class BookingCreateView(CreateView):
#     form_class = 
#     template_name =


# class BookingUpdateView(UpdateView):
#     form_class = 
#     template_name =