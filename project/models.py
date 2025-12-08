# File: models.py
# Author: Aaron Huang (ahuan@bu.edu),11/22/2025
# Description: Models for the project app.

from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Traveler (models.Model):
    """Model representing a traveler/user in the app."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        """String representation of the Traveler."""
        return f"{self.full_name} -created at {self.created_at}"
    
    
    
class Trip (models.Model):
    """Model representing a trip planned by a traveler."""

    # text choices ~= enums in django
    # attribute name = 'value in db', 'label shown to users'
    class TripStatus(models.TextChoices):
        """Choices for the status of the trip."""
        PLANNING = 'planning', 'Planning'
        UPCOMING = 'upcoming', 'Upcoming'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'

    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    location = models.TextField(blank=False)
    start_date = models.DateField(blank=True, null=True) #optional date field ie planning
    end_date = models.DateField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True) # optional ie no budget/unplanned
    notes = models.TextField(blank=True) #optional notes
    parent_trip = models.ForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name = 'sub_trips' ) # recursive, refer to a "parent trip" such that this is a "sub trip"
    #in a UX/logic perspective a trip is limited to one additional optional subtrip layer 
    
    status = models.CharField(max_length=20, choices=TripStatus.choices, default=TripStatus.PLANNING)
    def __str__(self):
        """String representation of the Trip."""
        return f"{self.traveler.full_name}: {self.location}"
    
    def get_absolute_url(self):
        """Absolute URL for the Trip detail view."""
        return reverse('tripdetail', kwargs={'pk': self.pk})

class ItineraryStop (models.Model):
    """Model representing a stop or activity within a trip itinerary."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    stop = models.TextField()
    orderIndex = models.IntegerField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        """String representation of the Itinerary Stop."""
        return f"({self.trip.location}): {self.stop}"
    
    def save(self, *args, **kwargs):
        """Save method to auto-assign orderIndex, automatically incrementing based on existing stops in the trip."""
        if self.orderIndex is None and self.trip_id:
            last_stop = ItineraryStop.objects.filter(trip=self.trip).order_by('-orderIndex').first()
            if last_stop and last_stop.orderIndex is not None:
                self.orderIndex = last_stop.orderIndex + 1
            else:
                self.orderIndex = 1
        super().save(*args, **kwargs)

class Booking (models.Model):
    """Model representing a booking associated with an itinerary stop."""

    class BookingType(models.TextChoices):
        """Choices for the type of booking."""
        FLIGHT = 'flight', 'Flight'
        HOTEL = 'hotel', 'Hotel'
        TRAIN = 'train', 'Train'
        CAR_RENTAL = 'car_rental', 'Car Rental'
        ACTIVITY  = 'activity', 'Activity'
        RESTAURANT = 'restaurant', 'Restuarant'
        OTHER = 'other', 'Other'

    stop = models.ForeignKey(ItineraryStop, on_delete=models.CASCADE)
    type = models.TextField(max_length=20, choices =BookingType.choices, default=BookingType.OTHER)
    confirmationcode = models.TextField()
    price = models.IntegerField()
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        """Booking string representation."""
        return f"{self.type} booking at {self.stop.stop}"
