from django.contrib import admin
from .models import Traveler, Trip, ItineraryStop, Booking

admin.site.register(Traveler)
admin.site.register(Trip)
admin.site.register(ItineraryStop)
admin.site.register(Booking)
