import datetime
from django import forms
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseModelFormSet
from .models import Menu, Cuisine, Recipe, RecipeIngredient, RecipeStep
from django.core.exceptions import ValidationError
from utils.func import both
from .widgets import ImageWidget

class RecipeModelForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['slug', 'author', 'creation_date']
        widgets = {
            'cooking_time': forms.TimeInput(attrs={'type': 'time'}),
            'image': ImageWidget,
        }
    
    def clean_cooking_time(self):
        cooking_time = self.cleaned_data['cooking_time']
        if cooking_time == datetime.time():
            raise ValidationError('Укажите время приготовления блюда.')
        return cooking_time


class RecipeFilterForm(forms.Form):
    menu = forms.ModelChoiceField(queryset=Menu.objects.all(), required=False, label='Меню', empty_label='Все')
    cuisine = forms.ModelChoiceField(queryset=Cuisine.objects.all(), required=False, label='Кухня', empty_label='Все')
    sortby = forms.ChoiceField(
        choices=(
            ('', 'Нет'),
            ('1', 'Сначала популярные'), 
            ('2', 'Сначала непопулярные'),
            ('3', 'Сначала новые'),
            ('4', 'Сначала старые'),
        ), 
        required=False,
        label='Сортировка'
    )


class RecipeIngredientModelForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'unit', 'amount', 'recipe']
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            need_amount = self.cleaned_data['unit'].need_amount
        except KeyError:
            need_amount = False
        if not both(need_amount, amount):
            if amount:
                return None
            raise ValidationError('Укажите количество выбранных ингредиентов.')
        return amount


class RecipeStepModelForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = '__all__'
        widgets = {
            'image': ImageWidget,
        }


class RecipeIngredientCleanMixin:
    def clean(self):
        if any(self.errors):
            return
    
        ingredients = []
        deleted_forms = 0
        for form in self.forms:
            if form.cleaned_data.get('DELETE', False) or not form.cleaned_data:
                deleted_forms += 1
                continue
            ingredient = form.cleaned_data.get('ingredient')
            if ingredient in ingredients:
                raise ValidationError('Ингредиенты не должны повторяться.')
            ingredients.append(ingredient)

            form.is_valid()
        
        if not self.forms or len(self.forms) == deleted_forms:
            raise ValidationError('Вы не указали ни одного ингредиента.')


class RecipeStepCleanMixin:
    def clean(self):
        if any(self.errors):
            return

        deleted_forms = 0
        for form in self.forms:
            if form.cleaned_data.get('DELETE', False) or not form.cleaned_data:
                deleted_forms += 1
                continue
            form.is_valid()

        if not self.forms or len(self.forms) == deleted_forms:
            raise ValidationError('Укажите как минимум 1 шаг в рецепте.')


class CleanAndSaveMixin:
    def clear_and_save(self, **kwargs):
        for form in self.forms:
            instance = form.cleaned_data.get('id')
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                if instance:
                    instance.delete()
                continue
            if not kwargs:
                form.save()
                continue
            instance = form.save(commit=False)
            for field, value in kwargs.items():
                setattr(instance, field, value)
            instance.save()
        

class BaseRecipeIngredientFormSet(RecipeIngredientCleanMixin, BaseFormSet, CleanAndSaveMixin):
    pass


class BaseRecipeStepFormSet(RecipeStepCleanMixin, BaseFormSet, CleanAndSaveMixin):
    pass


class BaseRecipeIngredientModelFormSet(RecipeIngredientCleanMixin, BaseModelFormSet, CleanAndSaveMixin):
    pass


class BaseRecipeStepModelFormSet(RecipeStepCleanMixin, BaseModelFormSet, CleanAndSaveMixin):
    pass
