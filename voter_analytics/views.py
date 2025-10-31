from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
# Create your views here.

class VoterListView(ListView):
    """ """
    model = Voter
    template_name= "show_all_voters.html"
    context_object_name = "voters"


class VoterDetailView(DetailView):
    """ """
    model = Voter
    template_name = "show_voter.html"
    context_object_name = "voter"


class GraphView(ListView):
    """ """
    model = Voter
    template_name = "show_voter.html"
    context_object_name = "voter"