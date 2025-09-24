from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles" #plural b/c contain many instances of Article


class ArticleView(DetailView):
    '''Display a single article.'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular 


class RandomArticleView(DetailView):
    '''Display a single article selected at random'''
    
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular 

    #methods
    def get_object(self):
        '''return one instance of the Article object 
        selected at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article 