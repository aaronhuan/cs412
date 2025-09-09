# File: quotes/views.py
# Author: Aaron Huang (ahuan@bu.edu),09/09/2025
# Description: View functions for the quotes app.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# list[str]: list of quotes from Steve Jobs.
quotes = [
    "Innovation is the ability to see change as an opportunity - not a threat.",
    "It doesn’t make sense to hire smart people and tell them what to do; we hire smart people so they can tell us what to do.",
    "It takes a lot of hard work to make something simple",
]

# list[str]: list of image links to display images of Steve Jobs.
images = [
    "https://tse1.explicit.bing.net/th/id/OIP.-fKKHgSE_5Up-3xzv5nHJwHaE8?rs=1&pid=ImgDetMain&o=7&rm=3",
    "https://tse3.mm.bing.net/th/id/OIP.v6hbwkuZNmyDNg8NczUf8wHaES?rs=1&pid=ImgDetMain&o=7&rm=3",
    "https://stevejobslegacyandleadership.weebly.com/uploads/4/2/3/0/42306593/3353581_orig.jpg",
]

def quote(request):
    """Respond to the URL '' and '/quote' through displaying a random quote and image."""
    
    # dict[str, str]: context data passed to the template, including a random quote and a random image.
    context ={
        "quote": quotes[random.randint(0,2)], #return a random quote via randomly picking an index.
        "image": images[random.randint(0,2)], #return a random image via randomly picking an index.
    } 

    # String, the path to the template to be rendered.
    template_name='quotes/quote.html'
    return render(request, template_name, context)

def show_all(request):
    """Respond to the URL '/show_all' by displaying all quotes and images."""
    
    # dict[str, list[str]]: the context data passed to the template, including all quotes and images.
    context ={
        "quotes": quotes,
        "images": images,
    }
    
    # String, the path to the template to be rendered.
    template_name='quotes/show_all.html'
    return render(request, template_name, context)


def about(request):
    """Respond to the URL '/about' with information about the site and Steve Jobs."""

    # String, the path to the template to be rendered.
    template_name = 'quotes/about.html'
    return render(request, template_name)
