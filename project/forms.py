# File: forms.py
# Author: Aaron Huang (ahuan@bu.edu),11/22/2025
# Description: Forms for creating and updating Travelers, Trips, ItineraryStops, and Bookings.

from django import forms
from .models import Traveler, Trip, ItineraryStop, Booking

#widgets to customize date inputs, without these the input would only be a text input
#widget.attrs set the html attributes ie in this case <input type = "date"> 
trip_date_widgets = {
    'start_date': forms.DateInput(attrs={'type': 'date'}),
    'end_date': forms.DateInput(attrs={'type': 'date'}),
}

stop_date_widget = {
    'date': forms.DateInput(attrs={'type': 'date'}),
}

booking_date_widget = {
    'date': forms.DateInput(attrs={'type': 'date'}),
}


class CreateTravelerForm(forms.ModelForm):
    """Form to create a new traveler."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form."""
        model = Traveler
        fields = ['full_name']

class UpdateTravelerForm(forms.ModelForm):
    """Form to update an existing traveler."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form."""
        model = Traveler
        fields = ['user', 'full_name']


class CreateTripForm(forms.ModelForm):
    """Form to create a new trip."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widgets."""
        model = Trip
        fields =  ['location', 'start_date', 'end_date', 'budget', 'notes', 'status']
        widgets = trip_date_widgets


class UpdateTripForm(forms.ModelForm):
    """Form to update an existing trip."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widgets."""
        model = Trip
        fields = ['location', 'start_date', 'end_date', 'budget', 'notes', 'status']
        widgets = trip_date_widgets


class CreateItineraryStopForm(forms.ModelForm):
    """Form to create a new itinerary stop."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widget."""
        model = ItineraryStop
        fields = ['date', 'stop', 'orderIndex', 'finished']
        widgets = stop_date_widget


class UpdateItineraryStopForm(forms.ModelForm):
    """Form to update an existing itinerary stop."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widget."""
        model = ItineraryStop
        fields = ['date', 'stop', 'orderIndex', 'finished']
        widgets = stop_date_widget


class CreateBookingForm(forms.ModelForm):
    """Form to create a new booking."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widget."""
        model = Booking
        fields = ['stop', 'type', 'confirmationcode', 'price', 'date']
        widgets = booking_date_widget


class UpdateBookingForm(forms.ModelForm):
    """Form to update an existing booking."""
    class Meta:
        """Inner Meta class to specify model and fields that are displayed on form. Includes date widget."""
        model = Booking
        fields = ['stop', 'type', 'confirmationcode', 'price', 'date']
        widgets = booking_date_widget
