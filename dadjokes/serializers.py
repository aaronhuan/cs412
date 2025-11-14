#File: dadjokes/serializers.py
#Author: Aaron Huang (ahuan@bu.edu), 11/14/2025
#Description: Serializers for validating and translating data for the API.

from rest_framework import serializers 
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''Serialize Joke instance to and from JSON for API.'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name']


class PictureSerializer(serializers.ModelSerializer):
    '''Serialize Picture instance to and from JSON for API.'''
    class Meta:
        model = Picture
        fields = ['id', 'image_file', 'image_url']

        