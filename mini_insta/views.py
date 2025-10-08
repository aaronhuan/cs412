# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: Class based views for Mini Instagram pages, ingerits from django generic views. 

from django.shortcuts import render
from .models import *
from .forms import CreatePostForm, UpdateProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Create your views here.

class ProfileListView(ListView):
    """Displays a list of all Profile instances."""
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    
class ProfileDetailView(DetailView):
    """Displays detailed information for a single profile."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display details for a single post."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name="post"

class CreatePostView(CreateView):
    """ Create a new post for a given profile and attaches one photo"""
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        """Add the profile into the context for the template """
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk'] #pk of the profile corresponding to the URL pattern
        profile = Profile.objects.get(pk=profile_pk) #add profile object 
        context['profile'] = profile 
        return context
    
    def form_valid(self, form):
        """Validates image_url before saving and creates the Photo."""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        response = super().form_valid(form)
        # image_url = self.request.POST.get("image_url").strip() # remove empty space
        # if image_url =="": #if its blank
        #     form.add_error(None, "Image URL is required")
        #     return self.form_invalid(form)
        # Photo.objects.create(post=self.object, image_url=image_url)

        images = self.request.FILES.getlist("imagefiles") #returns a list of 0 to many files 
        #process this with a loop to create an save Photo objects

        for image in images:
            Photo.objects.create(post=self.object, image_file=image)
            
        return response
    

class UpdateProfileView(UpdateView):
    form_class= UpdateProfileForm
    model = Profile
    template_name= "mini_insta/update_profile_form.html"

    
