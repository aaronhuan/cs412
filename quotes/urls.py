from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.quote, name='main'), 
    path('quote/', views.quote, name='quote'), #calls the same view function as the '' path
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]
