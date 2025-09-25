from django.urls import path
from . import views
urlpatterns = [
    path("", views.ProfileListView.as_view(), name="homepage"),
    path("show_all_profiles/", views.ProfileListView.as_view(), name = "display_all_profile" ),   
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name= "display_profile"),
]
