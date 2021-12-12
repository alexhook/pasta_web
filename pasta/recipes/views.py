from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http.request import HttpRequest
from django.views import generic
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep
from account.models import Profile

def index(request: HttpRequest):
    pass


class RecipeListView(generic.ListView):
    model = Recipe
    
    def get_queryset(self):
        return Recipe.objects.all().select_related('author__profile', 'menu', 'cuisine')


class RecipeDetailView(generic.DetailView):
    model = Recipe

    def get_object(self):
        return Recipe.objects.select_related('cuisine', 'menu', 'author__profile').prefetch_related('recipeingredient_set__ingredient', 'recipeingredient_set__unit','recipestep_set').get(slug=self.kwargs['slug'])
