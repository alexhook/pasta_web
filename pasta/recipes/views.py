from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep
from account.models import Profile
from django.views.generic.edit import CreateView
from .forms import RecipeModelForm, RecipeIngredientModelForm, RecipeStepModelForm

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


def recipe_create_form(request: HttpRequest):
    if request.method == 'POST':
        recipe_form = RecipeModelForm(request.POST, request.FILES, prefix='-recipe')
        # recipe_ingredient_form = RecipeIngredientModelForm(request.POST, prefix='-recipe-ingredient')
        # recipe_step_form = RecipeStepModelForm(request.POST, prefix='-recipe-step')
        # if recipe_form.is_valid() and recipe_ingredient_form.is_valid() and recipe_step_form.is_valid():
        if recipe_form.is_valid():
            # recipe_form.slug = slugify(recipe_form.title)
            # recipe_form.author = request.user.id
            # if request.POST.get('submit-save'):
            #     recipe_form.is_published = 0
            # if request.POST.get('submit-publish'):
            #     recipe_form.is_published = 1
            recipe_form.save()
            print(recipe_form.id)
            print(request)

            return HttpResponseRedirect(reverse('recipe-detail'))
    else:
        recipe_form = RecipeModelForm(prefix='-recipe')
    
    return render(request, 'recipes/recipe_form.html', {'recipe_form': recipe_form})


