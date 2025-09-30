# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: views.py creates classes inherited from ListView and DetailView to pass information to a template to work with instances of a model.

from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
# Create your views here.

class ProfileListView(ListView):
    """
    Displays a list of all Profile instances.

    Attributes:
        model (Profile): The model to query from the database.
        template_name (str): Path to the HTML template that renders the list.
        context_object_name (str): The name used to reference the list of profiles in the template.
    """
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    
class ProfileDetailView(DetailView):
    """
    Displays detailed information for a single Profile instance.

    Attributes:
        model (Profile): The model to query from the database.
        template_name (str): Path to the HTML template that renders the profile detail.
        context_object_name (str): The name used to reference the profile object in the template.
    """
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name="post"