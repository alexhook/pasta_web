from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Recipe, RecipeIngredient, RecipeStep
from .forms import RecipeFilterForm, RecipeModelForm, RecipeIngredientModelForm, RecipeStepModelForm, BaseRecipeIngredientFormSet, BaseRecipeStepFormSet, BaseRecipeIngredientModelFormSet, BaseRecipeStepModelFormSet
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView


class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=1).select_related('author', 'menu', 'cuisine')
        if queryset.exists():
            if self.request.GET:
                form = RecipeFilterForm(self.request.GET)
                if form.is_valid():
                    menu = form.cleaned_data.get('menu')
                    cuisine = form.cleaned_data.get('cuisine')
                    if menu:
                        queryset = queryset.filter(menu=menu)
                    if cuisine:
                        queryset = queryset.filter(cuisine=cuisine)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        menu = self.request.GET.get('menu', 0)
        cuisine = self.request.GET.get('cuisine', 0)
        context_data['form'] = RecipeFilterForm(initial={'menu': menu, 'cuisine': cuisine})
        return context_data


class RecipeDetailView(generic.DetailView):
    model = Recipe

    def get_object(self):
        return Recipe.objects.select_related('cuisine', 'menu', 'author').prefetch_related('recipeingredient_set__ingredient', 'recipeingredient_set__unit','recipestep_set').get(slug=self.kwargs['slug'])


@login_required
def recipe_create_form(request: HttpRequest):
    RecipeIngredientFormSet = formset_factory(
        RecipeIngredientModelForm,
        formset=BaseRecipeIngredientFormSet,
        absolute_max=30,
        max_num=30,
        validate_max=True,
        can_delete=True,
    )
    RecipeStepFormSet = formset_factory(
        RecipeStepModelForm,
        formset=BaseRecipeStepFormSet,
        absolute_max=30,
        max_num=30,
        validate_max=True,
        can_delete=True,
    )

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

            ingredient_formset.crean_and_save(recipe=recipe)
            step_formset.crean_and_save(recipe=recipe)

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


@login_required
def recipe_edit_form(request: HttpRequest, slug):
    RecipeIngredientFormSet = modelformset_factory(
        RecipeIngredient,
        RecipeIngredientModelForm,
        formset=BaseRecipeIngredientModelFormSet,
        absolute_max=30,
        max_num=30,
        validate_max=True,
        can_delete=True,
    )
    RecipeStepFormSet = modelformset_factory(
        RecipeStep,
        RecipeStepModelForm,
        formset=BaseRecipeStepModelFormSet,
        absolute_max=30,
        max_num=30,
        validate_max=True,
        can_delete=True,
    )
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredient_queryset = RecipeIngredient.objects.filter(recipe=recipe.id)
    step_queryset = RecipeStep.objects.filter(recipe=recipe.id)

    if request.method == 'POST':

        recipe_form = RecipeModelForm(request.POST, request.FILES, instance=recipe, prefix='recipe')
        ingredient_formset = RecipeIngredientFormSet(request.POST, queryset=ingredient_queryset, prefix='ingredient')
        step_formset = RecipeStepFormSet(request.POST, request.FILES, queryset=step_queryset, prefix='step')
        
        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            
            recipe = recipe_form.save(commit=False)
            if request.POST.get('submit-publish'):
                recipe.is_published = 1
            else:
                recipe.is_published = 0
            recipe.save()

            ingredient_formset.crean_and_save(recipe=recipe)
            step_formset.crean_and_save(recipe=recipe)

            return HttpResponseRedirect(reverse('recipe-detail', kwargs={'slug': recipe.slug}))
    else:
        recipe_form = RecipeModelForm(instance=recipe, prefix='recipe')
        ingredient_formset = RecipeIngredientFormSet(queryset=ingredient_queryset, prefix='ingredient')
        step_formset = RecipeStepFormSet(queryset=step_queryset, prefix='step')
    
    return render(
        request,
        'recipes/recipe_form.html',
        {
            'recipe_form': recipe_form, 
            'ingredient_formset': ingredient_formset, 
            'step_formset': step_formset
        }
    )


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
