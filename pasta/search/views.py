from django.shortcuts import render
from django.http import HttpRequest
from recipes.models import Recipe
from wiki.models import Ingredient, Instrument
from .forms import SearchForm

def index(request: HttpRequest):
    form = SearchForm()
    return render(
        request,
        'search/index.html',
        context={
            'form': form
        }
    )
