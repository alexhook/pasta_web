from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.views import generic
from .models import Recipe, RecipeIngredient, RecipeStep
from .forms import RecipeModelForm, RecipeIngredientModelForm, RecipeStepModelForm, BaseRecipeIngredientFormSet
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from wiki.models import Ingredient

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


@login_required(login_url='/admin/')
def recipe_form(request: HttpRequest, slug=None):
    RecipeIngredientFormSet = formset_factory(RecipeIngredientModelForm, formset=BaseRecipeIngredientFormSet, absolute_max=30, max_num=30)
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
        if slug:
            recipe = get_object_or_404(Recipe, slug=slug)
            print('---------------------------------')
            print(RecipeIngredient.objects.filter(recipe=recipe.id).values())
            print(Ingredient.objects.get(pk=1))
            print('---------------------------------')
            recipe_form = RecipeModelForm(instance=recipe, prefix='recipe')
            ingredient_formset = RecipeIngredientFormSet(initial=RecipeIngredient.objects.filter(recipe=recipe.id).values(), prefix='ingredient')
            step_formset = RecipeStepFormSet(initial=RecipeStep.objects.filter(recipe=recipe.id).values(), prefix='step')
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


