from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Traveler (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(blank=False)
    last_name = models.CharField(blank=False)
    created_at = models.DateTimeField(auto_now_add =True)


class Trip (models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    location = models.TextField(blank=False)
    start_date = models.DateField(blank=True, null=True) #optional date field ie planning
    end_date = models.DateField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True) # optional ie no budget/unplanned
    notes = models.TextField(blank=True) #optional notes
    parent_trip = models.ForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name = 'sub_trips' ) # recursive, refer to a "parent trip" such that this is a "sub trip"

    def get_absolute_url(self):
        return reverse('tripdetail', kwargs={'pk': self.pk})

class ItineraryStop (models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    stop = models.TextField()
    orderIndex = models.IntegerField()
    finished = models.BooleanField(default=False)

class Booking (models.Model):
    stop = models.ForeignKey(ItineraryStop, on_delete=models.CASCADE)
    type = models.TextField()
    confirmationcode = models.TextField()
    price = models.IntegerField()
    date = models.DateField(blank=True, null=True)
