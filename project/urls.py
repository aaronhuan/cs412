from django.urls import path
from . import views

urlpatterns = [
    path('', views.TravelerListView.as_view(), name="travelers"),
    path('<int:pk>/', views.TravelerDetailView.as_view(), name="traveler"),
    path('trips/', views.TripListView.as_view(), name='triplist'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='tripdetail'),
    path('trips/create', views.TripCreateView.as_view(), name='createtrip'),
    path('trips/update/<int:pk>', views.TripUpdateView.as_view(), name='updatetrip'),
    path('stop/', views.ItineraryStopListView.as_view(), name='stoplist'),
    path('stop/<int:pk>/', views.ItineraryStopDetailView.as_view(), name='stopdetail'),
    path('booking/', views.BookingListView.as_view(), name='bookinglist'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='bookingdetail'),
]
