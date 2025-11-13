from django.db import models
from random import randint
# Create your models here.

class Joke(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=100)

    def get_random_joke():
        num_jokes = Joke.objects.count()
        if num_jokes == 0:
            return None
        
        j_index = randint(0, num_jokes - 1)
        joke = Joke.objects.all()[j_index]
        return joke
    
class Picture(models.Model):
    image_file = models.ImageField(blank=True)
    image_url = models.URLField(blank =True)

    def get_image_url(self):
        """Return the image URL if exists, otherwise return the image file URL."""
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return ""
    
    def get_random_picture_url():
        num_pictures = Picture.objects.count()
        if num_pictures == 0:
            return ""
        
        p_index = randint(0, num_pictures - 1)
        picture = Picture.objects.all()[p_index]
        return picture.get_image_url()
    
    def get_random_picture():
        num_pictures = Picture.objects.count()
        if num_pictures == 0:
            return None
        
        p_index = randint(0, num_pictures - 1)
        picture = Picture.objects.all()[p_index]
        return picture