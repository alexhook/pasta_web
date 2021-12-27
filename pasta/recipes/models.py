from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from utils.func import unique_slugify

class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кухня')

    class Meta:
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name='Меню')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название рецепта')
    slug = models.SlugField(unique=True, blank=True, null=False)
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True, verbose_name='Кухня')
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, verbose_name='Меню')
    cooking_time = models.DurationField(null=True, verbose_name='Время приготовления')
    image = models.ImageField(upload_to='recipes/recipe/', verbose_name='Фотография готового блюда')
    description = models.TextField(verbose_name='Описание блюда')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=False)
    is_published = models.BooleanField(blank=True, default=0)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self)
        return super(Recipe, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.slug})


class AmoutUnit(models.Model):
    name = models.CharField(max_length=20)
    need_amount = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'Мерная идиница'
        verbose_name_plural = 'Мерные единицы'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('wiki.Ingredient', on_delete=models.DO_NOTHING)
    amount = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey('AmoutUnit', on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Ингредиент (рецепты)'
        verbose_name_plural = 'Ингредиенты (рецепты)'

    def __str__(self):
        return f'{self.ingredient.name}: {self.recipe.title}'


class RecipeStep(models.Model):
    image = models.ImageField(upload_to='recipes/recipesteps/')
    description = models.TextField(max_length=5000)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
