

from django import forms
from .models import Trip

date_widgets = {
    'start_date': forms.DateInput(attrs={'type': 'date'}),
    'end_date': forms.DateInput(attrs={'type': 'date'}),
}

class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['traveler', 'location', 'start_date', 'end_date', 'budget', 'notes', 'parent_trip']
        widgets = date_widgets

class UpdateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['traveler', 'location', 'start_date', 'end_date', 'budget', 'notes', 'parent_trip']
        widgets = date_widgets


