#File: voter_analysis/urls.py
#Author: Aaron Huang (ahuan@bu.edu), 10/28/2025
#Description: urls.py exposes endpoints for this voter_analysis application.

from voter_analytics.views import *
from django.urls import path

urlpatterns=[
    path('', VoterListView.as_view(), name ="voters"), 
    path('voter/<int:pk>', VoterDetailView.as_view(), name = "voter_detail"),
    path('graphs', GraphView.as_view(), name = "graphs")
]