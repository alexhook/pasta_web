from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from .models import Recipe, RecipeIngredient, RecipeStep
from django.core.exceptions import ValidationError

class RecipeModelForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeIngredientModelForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeStepModelForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = '__all__'


class BaseRecipeIngredientFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient')
            if ingredient in ingredients:
                raise ValidationError('Ингредиенты не должны повторяться.')
            ingredients.append(ingredient)
