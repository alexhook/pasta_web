from django.forms import ModelForm, fields, models
from .models import Recipe, RecipeIngredient, RecipeStep

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
