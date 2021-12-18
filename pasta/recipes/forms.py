from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseModelFormSet
from .models import Recipe, RecipeIngredient, RecipeStep, AmoutUnit
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
        if not self.forms:
            raise ValidationError('Вы не указали ни одного ингредиента.')
        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient')
            if ingredient in ingredients:
                raise ValidationError('Ингредиенты не должны повторяться.')
            ingredients.append(ingredient)

            if form.cleaned_data['unit'].need_amount and not form.cleaned_data['amount']:
                raise ValidationError('Укажите количество выбранных ингредиентов.')



class BaseRecipeStepFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not self.forms:
            raise ValidationError('Укажите как минимум 1 шаг в рецепте.')


class BaseRecipeIngredientModelFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not self.forms:
            raise ValidationError('Вы не указали ни одного ингредиента.')
        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient')
            if ingredient in ingredients:
                raise ValidationError('Ингредиенты не должны повторяться.')
            ingredients.append(ingredient)

            if form.cleaned_data['unit'].need_amount and not form.cleaned_data['amount']:
                raise ValidationError('Укажите количество выбранных ингредиентов.')



class BaseRecipeStepModelFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        if not self.forms:
            raise ValidationError('Укажите как минимум 1 шаг в рецепте.')
