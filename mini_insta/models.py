# File: models.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: File that creates a Profile model with 5 fields and a string function

from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.TextField(blank = True)
    display_name = models.TextField(blank = True)
    profile_image_url = models.URLField(blank = True)
    bio_text = models.TextField(blank = True)
    join_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.username} '