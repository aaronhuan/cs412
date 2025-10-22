# File: urls.py
# Author: Aaron Huang (ahuan@bu.edu),09/24/2025
# Description: urls.py exposes endpoints and delegates a response to a view function 

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name ="show_post"),
    path("profile/create_post", views.CreatePostView.as_view(), name="create_post"),
    path("profile/update", views.UpdateProfileView.as_view(), name= "update_profile"),
    path("post/<int:pk>/delete", views.DeletePostView.as_view(), name ="delete_post"),
    path("post/<int:pk>/update", views.UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name = "show_followers"),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name = "show_following"),
    path('profile/feed', views.PostFeedListView.as_view(), name = "show_feed"),
    path('profile/search', views.SearchView.as_view(), name = "search"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name ="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path('logged_out/', views.LoggedOutView.as_view(), name='logout_confirmation'),
]
