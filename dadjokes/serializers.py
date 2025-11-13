from rest_framework import serializers 
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Joke
        fields = ['id', 'text', 'name']

    

class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ['id', 'image_file', 'image_url']

        