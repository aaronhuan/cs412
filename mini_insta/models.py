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
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of this model instance."""
        return f'{self.username} joined on {self.join_date.strftime("%b %d, %Y")}'
    
    def get_all_posts(self):
        posts = Post.objects.filter(profile=self).order_by('timestamp')
        return posts 
    
class Post(models.Model):
    """ """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank= True) # optional so blank = true
    
    def __str__(self):
        """ """
        return f'{self.profile.username} posted on {self.timestamp}'
    
    def get_all_photos(self):
        photos = Photo.objects.filter(post = self).order_by('timestamp')
        return photos
    
    def get_first_photo(self):
        photo = Photo.objects.filter(post=self).first()
        return photo

class Photo(models.Model):
    """ """
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank =False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ """
        return f'image posted on {self.timestamp} by {self.post.profile.username}'