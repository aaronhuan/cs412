from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.

# 3 items in each
# create a list of quotes (string)
# and a list of images (image urls, as strings)

quotes = [
    "Innovation is the ability to see change as an opportunity - not a threat.",
    "It doesn’t make sense to hire smart people and tell them what to do; we hire smart people so they can tell us what to do.",
    "It takes a lot of hard work to make something simple",
]

images = [
    "https://tse1.explicit.bing.net/th/id/OIP.-fKKHgSE_5Up-3xzv5nHJwHaE8?rs=1&pid=ImgDetMain&o=7&rm=3",
    "https://tse3.mm.bing.net/th/id/OIP.v6hbwkuZNmyDNg8NczUf8wHaES?rs=1&pid=ImgDetMain&o=7&rm=3",
    "https://stevejobslegacyandleadership.weebly.com/uploads/4/2/3/0/42306593/3353581_orig.jpg",
]

def quote(request):
    '''Respond to the URL '' and '/quote', delegate work to template'''
    context ={
        "quote": quotes[random.randint(0,2)], #return a random quote via randomly picking an index 
        "image": images[random.randint(0,2)], #return a random image via randomly picking an index
    } 
    template_name='quotes/quote.html'
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL '/show_all', delegate work to template'''
    context ={
        "quotes": quotes,
        "images": images,
    }
    template_name='quotes/show_all.html'
    return render(request, template_name, context)


def about(request):
    '''Respond to the URL '/about', delegate work to template'''
    template_name = 'quotes/about.html'
    return render(request, template_name)
