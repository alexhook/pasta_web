from django.shortcuts import render
from django.http import HttpRequest
from recipes.models import Recipe
from wiki.models import Ingredient, Instrument
from .forms import SearchForm
from recipes.views import RecipeListView
from wiki.views import IngredientListView, InstrumentListView

def index(request: HttpRequest):
    form = SearchForm(request.GET)
    recipe_list = []
    ingredient_list = []
    instrument_list = []
    if form.is_valid():
        text = form.cleaned_data.get('text', '').strip()
        if text:
            recipe_list = Recipe.objects.filter(is_published=1, title__iregex=rf'{text}').select_related('author', 'menu', 'cuisine')
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
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        text = self.request.GET.get('text', '').strip()
        if not queryset.exists() or not text:
            return []
        return queryset.filter(title__iregex=rf'{text}')
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['text'] = self.request.GET.get('text', '').strip()
        context_data['menu'] = self.request.GET.get('menu', '')
        context_data['cuisine'] = self.request.GET.get('cuisine', '')
        page = self.request.GET.get('page')
        if page:
            context_data['page'] = page
        return context_data


class IngredientSearchListView(IngredientListView):
    template_name = 'search/ingredient_search_list.html'

    def get_queryset(self):
        text = self.request.GET.get('text', '').strip()
        if not text:
            return []
        queryset = Ingredient.objects.filter(name__iregex=rf'{text}')
        return queryset
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['text'] = self.request.GET.get('text', '').strip()
        page = self.request.GET.get('page')
        if page:
            context_data['page'] = page
        return context_data


class InstrumentSearchListView(InstrumentListView):
    template_name = 'search/instrument_search_list.html'

    def get_queryset(self):
        text = self.request.GET.get('text', '').strip()
        if not text:
            return []
        queryset = Instrument.objects.filter(name__iregex=rf'{text}')
        return queryset
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['text'] = self.request.GET.get('text', '').strip()
        page = self.request.GET.get('page')
        if page:
            context_data['page'] = page
        return context_data
