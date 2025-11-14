#File: dadjokes/views.py
#Author: Aaron Huang (ahuan@bu.edu), 11/14/2025
#Description: Views for the dadjokes app handling display and API endpoints.

from django.shortcuts import render
from .models import Joke, Picture
from django.views.generic import ListView, DetailView, TemplateView
from .serializers import JokeSerializer, PictureSerializer
from rest_framework import generics
from rest_framework.response import Response

class RandomJokeView(TemplateView):
    '''View to render a random joke and image.'''
    template_name = 'dadjokes/random_joke.html'

    def get_context_data(self, **kwargs):
        '''Use random joke + picture methods from their respective models for template context'''
        context = super().get_context_data(**kwargs)    
        context['joke'] = Joke.get_random_joke()
        context['picture_url'] = Picture.get_random_picture_url()
        return context 

class JokeListView(ListView):
    '''Display a list of jokes.'''
    model = Joke
    context_object_name = 'jokes'
    template_name = 'dadjokes/show_all_jokes.html'

class JokeDetailView(DetailView):
    '''Display the details for a single joke.'''
    model = Joke
    context_object_name = 'joke'
    template_name = 'dadjokes/show_joke.html'

class PictureListView(ListView):
    '''Display a list of all pictures.'''
    model = Picture
    context_object_name = 'pictures'
    template_name = 'dadjokes/show_all_images.html'

class PictureDetailView(DetailView):
    '''Display the details for a single picture.'''
    model = Picture
    context_object_name = 'picture'
    template_name = 'dadjokes/show_image.html'


###################### API VIEWS ######################
class RandomJokeAPIView(generics.GenericAPIView):
    '''API endpoint that returns a random joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer 

    def get(self, request, *args, **kwargs):
        '''Make a function to handle GET requests.'''
        random_joke = Joke.get_random_joke()
        serializer = self.get_serializer(random_joke)
        return Response(serializer.data)

class JokeListCreateAPIView(generics.ListCreateAPIView):
    '''API endpoint to list all jokes/create one.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    '''API endpoint to get a single joke by its ID.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    '''API endpoint to list all pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    '''API endpoint to get one picture by it's ID.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.GenericAPIView):
    '''API endpoint to get a random picture.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get(self, request, *args, **kwargs):
        '''Define the get method to handle GET requests, serialize a random picture.'''
        random_picture = Picture.get_random_picture()
        serializer = self.get_serializer(random_picture)
        return Response(serializer.data)
    
