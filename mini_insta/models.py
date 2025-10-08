# File: models.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: File that creates Profile, Post, and Photo model and lists the fields & methods inside a model

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """Represents a user profile in the Mini Instagram application."""
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of this profile instance."""
        return f'{self.username} joined on {self.join_date.strftime("%b %d, %Y")}'
    
    def get_all_posts(self):
        """Return all posts for this profile ordered by timestamp descending via prepend '-' """
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts 
    
class Post(models.Model):
    """Represent a single post authored by a profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank= True) # optional so blank = true
    
    def __str__(self):
        """Return a string representation of this post instance."""
        return f'{self.profile.username} posted on {self.timestamp}'
    
    def get_absolute_url(self):
        """Return the absolute URL for this post detail page."""
        return reverse('show_post', kwargs = {'pk': self.pk})
    
    def get_all_photos(self):
        """Return all photos for this post ordered by timestamp ascending"""
        photos = Photo.objects.filter(post = self).order_by('timestamp')
        return photos
    
    def get_first_photo(self):
        """Return the first photo for this post or None is absent."""
        photo = Photo.objects.filter(post=self).first()
        return photo

class Photo(models.Model):
    """Represent a single photo authored by a post"""
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank =True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        """Return a string representation of this photo"""
        return f'image posted on {self.timestamp} by {self.post.profile.username}, image: {self.image_url if self.image_url else self.image_file}'
    
    def get_image_url(self):
        """Return the image URL if exists, otherwise return the image file URL."""
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return ""