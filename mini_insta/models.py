# File: models.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: File that creates a Profile model with 5 fields and a string function

from django.db import models

# Create your models here.
class Profile(models.Model):
    """
    Represents a user profile in the Mini Instagram application.

    Fields:
        username (TextField): The user's unique identifier.
        display_name (TextField): The name displayed publicly.
        profile_image_url (URLField): Link to the user's profile image.
        bio_text (TextField): Short biography or description.
        join_date (DateTimeField): Timestamp of when the profile was created.

    Methods:
        __str__: Returns a string representation combining username and join date.
    """
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of this model instance."""
        return f'{self.username} joined on {self.join_date.strftime("%b %d, %Y")}'
