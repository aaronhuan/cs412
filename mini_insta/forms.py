# File: forms.py
# Author: Aaron Huang (ahuan@bu.edu),09/30/2025
# Description: Form for creating a post, inherits from ModelForm

from django import forms
from .models import * 

class CreatePostForm(forms.ModelForm):
    """Create a form to submit a new post caption. """
    class Meta:
        """Configure model and exposed fields."""
        model = Post
        fields=['caption']


class UpdateProfileForm(forms.ModelForm):
    """Create a form to update a profile."""
    class Meta:
        """Configure model and exposed fields."""
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
        