# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: views.py creates classes inherited from ListView and DetailView to pass information to a template to work with instances of a model.

from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
# Create your views here.

class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"