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
    class Meta:
        model = Traveler
        fields = ['user', 'full_name']

class UpdateTravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ['user', 'full_name']


class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields =  ['location', 'start_date', 'end_date', 'budget', 'notes', 'status']
        widgets = trip_date_widgets


class UpdateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['location', 'start_date', 'end_date', 'budget', 'notes', 'status']
        widgets = trip_date_widgets


class CreateItineraryStopForm(forms.ModelForm):
    class Meta:
        model = ItineraryStop
        fields = ['date', 'stop', 'orderIndex', 'finished']
        widgets = stop_date_widget


class UpdateItineraryStopForm(forms.ModelForm):
    class Meta:
        model = ItineraryStop
        fields = ['date', 'stop', 'orderIndex', 'finished']
        widgets = stop_date_widget


class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['stop', 'type', 'confirmationcode', 'price', 'date']
        widgets = booking_date_widget


class UpdateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['stop', 'type', 'confirmationcode', 'price', 'date']
        widgets = booking_date_widget
