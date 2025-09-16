#File: restaurant/urls.py
#Author: Aaron Huang (ahuan@bu.edu), 09/16/2025
#Description: urls for the restaurant app routing to main, order, and confirmation views.


from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]