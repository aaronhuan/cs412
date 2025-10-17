# File: models.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: Class based views for Mini Instagram pages, inherits from django generic views.

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """Represents a user profile in the Mini Instagram application."""
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        """return a string representation of this profile instance."""
        return f'{self.username} joined on {self.join_date.strftime("%b %d, %Y")}'
    
    def get_all_posts(self):
        """Return all posts for this profile ordered by timestamp descending via prepend '-' """
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts 
    
    def get_num_posts(self):
        """Return the number of posts this profile has."""
        return Post.objects.filter(profile=self).count()
    
    def get_followers(self):
        """Return a list of Profile instances that follow this profile."""
        follow_instances = Follow.objects.filter(profile=self)
        followers = [follow.follower_profile for follow in follow_instances] # iterate through follow_instances and get the follower_profile attribute
        return followers
    
    def get_num_followers(self):
        """"Return the number of followers this profile has."""
        return Follow.objects.filter(profile=self).count()
    
    def get_num_following(self):
        """Return the number of profiles this profile is following."""
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_following(self):
        """Return a list of Profile instances that this profile is following."""
        follow_instances = Follow.objects.filter(follower_profile=self)
        following = [following.profile for following in follow_instances] # iterate through follow_instances and get the profile attribute
        return following
    
    def get_post_feed(self):
        """Return a list of Post isntances for this profile's feed, ordered with most recent on top."""
        following_profiles = self.get_following()
        posts = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return posts

    def get_absolute_url(self):
        """Return the absolute URL for this profile detail page."""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class Post(models.Model):
    """Represent a single post authored by a profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add =True)
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
    
    def get_all_comments(self):
        """Return all comments for this post ordered by timestamp ascending"""
        comments = Comment.objects.filter(post=self).order_by('timestamp')
        return comments
    
    def get_likes(self):
        """Return all likes for this post"""
        likes = Like.objects.filter(post=self)
        return likes 
    
    def get_num_likes(self):
        """Return the number of likes for this post"""
        return self.get_likes().count()

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
        
class Follow (models.Model):
    """Represent a follow relationship between two profiles."""
    profile = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name= "follower_profile")
    timestamp = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        """return a string representation of this follow instance."""
        return f'{self.follower_profile.username} followed {self.profile.username} on {self.timestamp}'
    
class Comment (models.Model):
    """Represent a comment made by a profile on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        """Return a string representation of this comment."""
        return f'{self.profile.username} commented on {self.post} at {self.timestamp}'
    

class Like(models.Model):
    """Represent a like made by a profile on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this like."""
        return f'{self.profile.username} liked {self.post} at {self.timestamp}'