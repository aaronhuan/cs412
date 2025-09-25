from django.urls import path
from . import views
urlpatterns = [
    path("", views.ProfileListView.as_view(), name="showall"),
    path("show_all_profiles/", views.ProfileListView.as_view(), name = "all" ),   
]
