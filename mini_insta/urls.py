# File: urls.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: urls.py exposes endpoints and delegates a response to a view function 

from django.urls import path
from . import views
urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name ="show_post")
]
