from django.urls import path
from .views import *
urlpatterns = [
    path('', RandomJokeView.as_view(), name='random_joke_home'),
    path('random/', RandomJokeView.as_view(), name='random_joke'),
    path('jokes/', JokeListView.as_view(), name='joke_list'),
    path('jokes/<int:pk>/', JokeDetailView.as_view(), name='joke_detail'),
    path('pictures/', PictureListView.as_view(), name='picture_list'),
    path('pictures/<int:pk>/', PictureDetailView.as_view(), name='picture_detail'),
    path("api/", RandomJokeAPIView.as_view(), name="api_random_joke_root"),
    path("api/random/", RandomJokeAPIView.as_view(), name="api_random_joke"),
    path("api/jokes/", JokeListCreateAPIView.as_view(), name="api_joke_list_create"),
    path("api/joke/<int:pk>", JokeDetailAPIView.as_view(), name="api_joke_detail"),
    path("api/pictures/", PictureListAPIView.as_view(), name="api_picture_list"),
    path("api/picture/<int:pk>/", PictureDetailAPIView.as_view(), name="api_picture_detail"),
    path("api/random_picture/", RandomPictureAPIView.as_view(), name="api_random_picture"),
]