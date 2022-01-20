from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from utils.func import unique_slugify

class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')

    class Meta:
        verbose_name = 'кухня'
        verbose_name_plural = 'кухни'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name='наименование')
    slug = models.SlugField(unique=True, blank=True, null=False, help_text='Заполняется автоматически.')
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True, verbose_name='кухня')
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, verbose_name='меню')
    cooking_time = models.DurationField(null=True, verbose_name='время приготовления')
    image = models.ImageField(upload_to='recipes/recipe/', verbose_name='фотография готового блюда')
    description = models.TextField(verbose_name='описание блюда')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=False, verbose_name='автор')
    is_published = models.BooleanField(blank=True, default=0, verbose_name='опубликован')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.slug})


class AmoutUnit(models.Model):
    name = models.CharField(max_length=20, verbose_name='наименование')
    need_amount = models.BooleanField(
        default=1,
        verbose_name='количественная',
        help_text='Установите флажок, если мерной единице требуется указание какой-либо количественной суммы. '
                  'Например, для мерной ед. "по вкусу" указание суммы не требуется.'
    )

    class Meta:
        verbose_name = 'мерная единица'
        verbose_name_plural = 'мерные единицы'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('wiki.Ingredient', on_delete=models.DO_NOTHING, verbose_name='ингредиент')
    amount = models.IntegerField(blank=True, null=True, verbose_name='сумма')
    unit = models.ForeignKey('AmoutUnit', on_delete=models.DO_NOTHING, verbose_name='мерная единица')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True, verbose_name='рецепт')

    class Meta:
        verbose_name = 'ингредиент (рецепты)'
        verbose_name_plural = 'ингредиенты (рецепты)'

    def __str__(self):
        return f'{self.ingredient.name}: {self.recipe.title}'
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.recipe.slug})


class RecipeStep(models.Model):
    image = models.ImageField(upload_to='recipes/recipesteps/', verbose_name='иллюстрация')
    description = models.TextField(max_length=5000, verbose_name='описание')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True, verbose_name='рецепт')

    class Meta:
        verbose_name = 'шаг'
        verbose_name_plural = 'шаги'
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.recipe.slug})
