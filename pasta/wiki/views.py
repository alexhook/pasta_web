from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http.request import HttpRequest
from .models import WikiSection, IngredientGroup, Ingredient, Instrument
from django.views import generic
from django.http import Http404

def index(request: HttpRequest):
    sections = WikiSection.objects.all()
    data = [
        {
            'name': 'Ингредиенты',
            'get_absolute_url': reverse('ingredient-groups-list'),
            'image': sections.get(name='Ингредиенты').image,
        },
        {
            'name': 'Инструменты',
            'get_absolute_url': reverse('instruments-list'),
            'image': sections.get(name='Инструменты').image,
        },
    ]
    return render(
        request,
        'wiki/wiki_index.html',
        context={
            'instance_list': data,
        }
    )


class IngredientGroupListView(generic.ListView):
    model = IngredientGroup
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name')


class IngredientListView(generic.ListView):
    model = Ingredient
    ordering = ['name']
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Ingredient.objects.filter(group__slug=self.kwargs['group_slug'])
        if not queryset:
            raise Http404
        return queryset


class IngredientDetailView(generic.DetailView):
    model = Ingredient

    def get_object(self):
        return get_object_or_404(Ingredient, group__slug=self.kwargs['group_slug'], slug=self.kwargs['slug'])


class InstrumentListView(generic.ListView):
    model = Instrument
    ordering = ['name']
    paginate_by = 15


class InstrumentDetailView(generic.DetailView):
    model = Instrument