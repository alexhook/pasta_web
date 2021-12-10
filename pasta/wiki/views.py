from django.shortcuts import get_object_or_404, render
from django.http.request import HttpRequest
from .models import IngredientGroup, Ingredient, Instrument
from django.views import generic
from django.http import Http404

def index(request: HttpRequest):
    return render(
        request,
        'wiki-index.html',
        context={}
    )


class IngredientGroupListView(generic.ListView):
    model = IngredientGroup


class IngredientListView(generic.ListView):
    model = Ingredient
    
    def get_queryset(self):
        print(self.kwargs)
        self.group = get_object_or_404(IngredientGroup, slug=self.kwargs['group'])
        return Ingredient.objects.filter(group__slug=self.group.slug).order_by('name')


class IngredientDetailView(generic.DetailView):
    model = Ingredient

    def get_object(self):
        self.group = get_object_or_404(IngredientGroup, slug=self.kwargs['group'])
        return get_object_or_404(Ingredient, group=self.group, slug=self.kwargs['slug'])


class InstrumentListView(generic.ListView):
    model = Instrument
    ordering = ['name']


class InstrumentDetailView(generic.DetailView):
    model = Instrument