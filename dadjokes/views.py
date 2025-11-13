from django.shortcuts import render
from .models import Joke, Picture
from django.views.generic import ListView, DetailView, TemplateView
from .serializers import JokeSerializer, PictureSerializer
from rest_framework import generics
from rest_framework.response import Response

class RandomJokeView(TemplateView):
    template_name = 'dadjokes/random_joke.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['joke'] = Joke.get_random_joke()
        context['picture_url'] = Picture.get_random_picture_url()
        return context 

class JokeListView(ListView):
    '''no img'''
    model = Joke
    context_object_name = 'jokes'
    template_name = 'dadjokes/show_all_jokes.html'

class JokeDetailView(DetailView):
    model = Joke
    context_object_name = 'joke'
    template_name = 'dadjokes/show_joke.html'

class PictureListView(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'dadjokes/show_all_images.html'

class PictureDetailView(DetailView):
    model = Picture
    context_object_name = 'picture'
    template_name = 'dadjokes/show_image.html'


###################### API VIEWS ######################
class RandomJokeAPIView(generics.GenericAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer 

    def get(self, request, *args, **kwargs):
        random_joke = Joke.get_random_joke()
        serializer = self.get_serializer(random_joke)
        return Response(serializer.data)

class JokeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.GenericAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get(self, request, *args, **kwargs):
        random_picture = Picture.get_random_picture()
        serializer = self.get_serializer(random_picture)
        return Response(serializer.data)
    
