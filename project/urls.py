# File: urls.py
# Author: Aaron Huang (ahuan@bu.edu),11/22/2025
# Description: url patterns for the project app.

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    path('travelers', staff_member_required(views.TravelerListView.as_view()), name="travelers"),
    path('signup/', views.TravelerCreateView.as_view(), name='signup'),
    path('travelers/<int:pk>/', staff_member_required(views.TravelerDetailView.as_view()), name="traveler"),
    path('travelers/create', views.TravelerCreateView.as_view(), name='createtraveler'),
    path('travelers/update/<int:pk>', staff_member_required(views.TravelerUpdateView.as_view()), name='updatetraveler'),
    path('travelers/delete/<int:pk>', staff_member_required(views.TravelerDeleteView.as_view()), name='deletetraveler'),
    path('trips/', views.TripListView.as_view(), name='triplist'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='tripdetail'),
    path('trips/create/', views.TripCreateView.as_view(), name='createtrip'),
    path('trips/<int:parent_pk>/create/', views.TripCreateView.as_view(), name='createsubtrip'),
    path('trips/update/<int:pk>', views.TripUpdateView.as_view(), name='updatetrip'),
    path('trips/delete/<int:pk>', views.TripDeleteView.as_view(), name='deletetrip'),
    path('stop/<int:pk>/', views.ItineraryStopDetailView.as_view(), name='stopdetail'),
    path('trips/<int:trip_pk>/stop/create/', views.ItineraryStopCreateView.as_view(), name='createstop'),
    path('stop/update/<int:pk>', views.ItineraryStopUpdateView.as_view(), name='updatestop'),
    path('stop/delete/<int:pk>', views.ItineraryStopDeleteView.as_view(), name='deletestop'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='bookingdetail'),
    path('trips/<int:trip_pk>/booking/create/', views.BookingCreateView.as_view(), name='createbooking'),
    path('booking/update/<int:pk>', views.BookingUpdateView.as_view(), name='updatebooking'),
    path('booking/delete/<int:pk>', views.BookingDeleteView.as_view(), name='deletebooking'),
]
