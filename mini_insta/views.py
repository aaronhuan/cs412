# File: views.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: Class based views for Mini Instagram pages, inherits from django generic views. 

from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.shortcuts import redirect 
# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Class that inherits from built in LoginRequiredMixin, used to override or add methods."""
    def get_login_url(self):
        """Obtain the url that displays the login form."""
        return reverse('login')

    def get_logged_in_profile(self):
        """Query for the profile associated with the logged in user."""
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

    def get_context_data(self, **kwargs):
        """Add 'is_following' context variable to indicate whether the logged-in user follows this profile."""
        context = super().get_context_data(**kwargs)
        context["is_following"] = (self.request.user.is_authenticated and
            Follow.objects.filter(follower_profile__user=self.request.user,
                profile=self.object
            ).exists()
        )
        return context


class PostDetailView(DetailView):
    """Display details for a single post."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name="post"

    def get_context_data(self, **kwargs):
        """Add 'is_liked' context variable to indicate whether the logged-in user liked this post."""
        context = super().get_context_data(**kwargs)
        context["is_liked"] = (self.request.user.is_authenticated and
            Like.objects.filter(profile__user=self.request.user,
                post=self.object
            ).exists()
        )
        return context

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
    """Render the logged out confirmation page."""
    template_name = 'mini_insta/logged_out.html'

class CreateProfileView(CreateView):
    """Create a new Profile and  Django User, log the user in and direct them to their detailed profile page."""
    model = Profile 
    form_class=CreateProfileForm 
    template_name="mini_insta/create_profile_form.html"
    
    def get_context_data(self, **kwargs):
        """Adds 'create_user_form' context to the template to display the built-in django user creation form."""
        context = super().get_context_data(**kwargs)
        context['create_user_form'] = UserCreationForm()
        return context 
    
    def form_valid(self, form):
        """When the form is valid: create the User, the Profile, log in, and save."""
        user = UserCreationForm(self.request.POST).save()

        form.instance.user = user 

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        """After successful creation, go to the new profile’s detail page."""
        return self.object.get_absolute_url()
    

class FollowView(MyLoginRequiredMixin, TemplateView):
    """Create a Follow from the logged-in user's Profile to the target Profile."""
    def dispatch(self, request, *args, **kwargs):
        """Create the Follow unless the user is viewing their own profile, then redirect back."""
        user = self.get_logged_in_profile()
        view_profile = Profile.objects.get(pk=kwargs['pk'])

        if user ==view_profile: 
            return redirect(user.get_absolute_url())
        
        Follow.objects.get_or_create(follower_profile=user, profile=view_profile)
        return redirect(view_profile.get_absolute_url())
    
class UnfollowView(MyLoginRequiredMixin, TemplateView):
    """Delete existing Follow from the user's Profile to the target Profile."""
    def dispatch(self, request, *args, **kwargs):
        """Remove the Follow unless it is the user's own profile, then redirect back."""
        user = self.get_logged_in_profile()
        view_profile = Profile.objects.get(pk=kwargs['pk'])

        if user ==view_profile: 
            return redirect(user.get_absolute_url())
        
        Follow.objects.get(follower_profile=user, profile=view_profile).delete()
        return redirect(view_profile.get_absolute_url())

class LikeView(MyLoginRequiredMixin, TemplateView):
    """Create a Like by the logged-in user's Profile on a Post."""
    def dispatch(self, request, *args, **kwargs):
        """Create the Like unless the post is the user's, then redirect back to the post."""
        user = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        if user ==post.profile: 
            return redirect(user.get_absolute_url())
        
        Like.objects.get_or_create(post=post, profile=user)
        return redirect(post.get_absolute_url())

class UnlikeView(MyLoginRequiredMixin, TemplateView):
    """Delete existing Like by the user on the target Post."""
    def dispatch(self, request, *args, **kwargs):
        """Remove the Like unless the post belongs to the user, then redirect back."""
        user = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        if user ==post.profile: 
            return redirect(user.get_absolute_url())
        
        Like.objects.get(post=post, profile=user).delete()
        return redirect(post.get_absolute_url())
