from django.shortcuts import render
from django.http import HttpRequest
from recipes.models import Recipe
from wiki.models import Ingredient, Instrument
from .forms import SearchForm
from recipes.views import RecipeListView
from wiki.views import IngredientListView, InstrumentListView

def index(request: HttpRequest):
    form = SearchForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data.get('text')
        recipe_list = Recipe.objects.filter(is_published=1, title__iregex=rf'{text}').select_related('author__profile', 'menu', 'cuisine')
        ingredient_list = Ingredient.objects.filter(name__iregex=rf'{text}').select_related('group')
        instrument_list = Instrument.objects.filter(name__iregex=rf'{text}')
    return render(
        request,
        'search/index_search.html',
        context={
            'text': text,
            'recipe_list': recipe_list,
            'ingredient_list': ingredient_list,
            'instrument_list': instrument_list,
        },
    )


class RecipeSearchListView(RecipeListView):
    template_name = 'search/recipe_search_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        text = self.request.GET.get('text')
        if not queryset.exists() or not text:
            return queryset
        return queryset.filter(title__iregex=rf'{text}')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['text'] = self.request.GET.get('text')
        return data