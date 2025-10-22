# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: Class based views for Mini Instagram pages, inherits from django generic views. 

from django.shortcuts import render
from .models import *
from .forms import CreatePostForm, UpdatePostForm, UpdateProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin 

# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('login')

    def get_logged_in_profile(self):
        if not self.request.user.is_authenticated:
            return None
        
        return Profile.objects.filter(user = self.request.user).first()
    
    # def get_query_set(self):
    #     return Post.objects.filter(profile__user=self.request.user)


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

class CreatePostView(MyLoginRequiredMixin, CreateView):
    """ Create a new post for a given profile and attaches one photo"""
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        """Add the profile into the context for the template """
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_logged_in_profile() # no longer read from pk
        return context
    
    def form_valid(self, form):
        """Validates image_url before saving and creates the Photo."""
        profile = self.get_logged_in_profile()
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
    

class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    """Update a profile."""
    form_class= UpdateProfileForm
    model = Profile
    template_name= "mini_insta/update_profile_form.html"
    
    def get_object(self, queryset = None):
        '''find the Profile object of the logged in user'''
        return self.get_logged_in_profile()


class UpdatePostView(MyLoginRequiredMixin, UpdateView):
    """Update a post."""
    form_class = UpdatePostForm
    model = Post 
    template_name = "mini_insta/update_post_form.html"


class DeletePostView(MyLoginRequiredMixin, DeleteView):
    """Delete a post."""
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        """Add the profile into the context for the template """
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        """Return to the profile page after deleting a post."""
        return self.object.profile.get_absolute_url()
    

class ShowFollowersDetailView(DetailView):
    """Display a list of followers for a given profile."""
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Display a list of profiles that a given profile is following."""
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(MyLoginRequiredMixin, ListView):
    """Display a list of posts for a given profile's feed."""
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"
    
    def get_context_data(self, **kwargs):
        """Add the profile viewing the feed into the context for the template."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context 
    
    def get_queryset(self):
        """Return the List of posts for this profile's feed."""
        profile = self.get_logged_in_profile()
        posts = profile.get_post_feed()
        return posts
    
class SearchView(MyLoginRequiredMixin, ListView):
    """Display a list of profiles and posts based on text input."""
    template_name = "mini_insta/search_results.html"
    
    def dispatch(self, request, *args, **kwargs):
        """ Change route based on if there is a query."""
        self.query = request.GET.get("query") #test for name query 
        if not self.query: #absent query
            profile = self.get_logged_in_profile()
            return render(request, "mini_insta/search.html", {"profile" : profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return Posts that match the criteria of the current query."""
        matching_posts = Post.objects.filter(caption__contains=self.query)
        return matching_posts
    
    def get_context_data(self, **kwargs):
        """ Add useful context variables (profile, query, posts, profiles) for the template. """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        context["query"] = self.query
        context["posts"] = self.get_queryset()
        context["profiles"] = Profile.objects.filter( #to perform OR queries use Q object from django.db.models 
            Q(display_name__contains=self.query) |  # | = logical or, & = logical and 
            Q(username__contains=self.query) | 
            Q(bio_text__contains=self.query)
        )
        return context
    

class LoggedOutView(TemplateView):
    template_name = 'mini_insta/logged_out.html'
