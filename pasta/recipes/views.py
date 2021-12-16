from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.views import generic
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep
from django.views.generic.edit import CreateView
from .forms import RecipeModelForm, RecipeIngredientModelForm, RecipeStepModelForm
from django.forms import formset_factory

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
    RecipeIngredientFormSet = formset_factory(RecipeIngredientModelForm, absolute_max=30, max_num=30)
    RecipeStepFormSet = formset_factory(RecipeStepModelForm, absolute_max=30, max_num=30)

    if request.method == 'POST':

        recipe_form = RecipeModelForm(request.POST, request.FILES, prefix='recipe')
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix='ingredient')
        step_formset = RecipeStepFormSet(request.POST, request.FILES, prefix='step')
        
        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            if request.POST.get('submit-publish'):
                recipe.is_published = 1
            recipe.save()

            for form in ingredient_formset:
                print('-------------------------------------')
                print(form.cleaned_data)
                print('-------------------------------------')
                if form.cleaned_data:
                    ingredient = form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            for form in step_formset:
                if form.cleaned_data:
                    step = form.save(commit=False)
                    step.recipe = recipe
                    step.save()

            return HttpResponseRedirect(reverse('recipe-detail', kwargs={'slug': recipe.slug}))
    else:
        recipe_form = RecipeModelForm(prefix='recipe')
        ingredient_formset = RecipeIngredientFormSet(prefix='ingredient')
        step_formset = RecipeStepFormSet(prefix='step')
    
    return render(
        request,
        'recipes/recipe_form.html',
        {
            'recipe_form': recipe_form, 
            'ingredient_formset': ingredient_formset, 
            'step_formset': step_formset
        }
    )


