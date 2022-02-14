from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from utils.func import unique_slugify
from pytils.translit import slugify

class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(max_length=70, unique=True, blank=True, null=False, help_text='Заполняется автоматически.')
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True, verbose_name='Кухня')
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, verbose_name='Меню')
    cooking_time = models.TimeField(null=True, verbose_name='Время приготовления')
    image = models.ImageField(upload_to='recipes/recipe/', verbose_name='Фотография готового блюда')
    description = models.TextField(verbose_name='Описание блюда')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    is_published = models.BooleanField(blank=True, default=0, verbose_name='Опубликован')
    creation_date = models.DateField(verbose_name='Дата создания', auto_now_add=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or not self.slug.startswith(slugify(self.title)):
            self.slug = unique_slugify(self)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.slug})


class AmoutUnit(models.Model):
    name = models.CharField(max_length=20, verbose_name='Наименование')
    need_amount = models.BooleanField(
        default=1,
        verbose_name='Количественная',
        help_text='Установите флажок, если мерной единице требуется указание какой-либо количественной суммы. '
                  'Например, для мерной ед. "по вкусу" указание суммы не требуется.'
    )

    class Meta:
        verbose_name = 'Мерная единица'
        verbose_name_plural = 'Мерные единицы'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('wiki.Ingredient', on_delete=models.DO_NOTHING, verbose_name='Ингредиент')
    amount = models.IntegerField(blank=True, null=True, verbose_name='Сумма')
    unit = models.ForeignKey('AmoutUnit', on_delete=models.DO_NOTHING, verbose_name='Мерная единица')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Ингредиент (рецепты)'
        verbose_name_plural = 'Ингредиенты (рецепты)'

    def __str__(self):
        return f'{self.ingredient.name}: {self.recipe.title}'
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.recipe.slug})


class RecipeStep(models.Model):
    image = models.ImageField(upload_to='recipes/recipesteps/', verbose_name='Иллюстрация')
    description = models.TextField(max_length=5000, verbose_name='Описание')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.recipe.slug})
