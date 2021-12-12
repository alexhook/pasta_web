from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.utils.text import slugify
from django.urls import reverse

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False, auto_created=True)
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True)
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True)
    cooking_time = models.TimeField()
    image = models.ImageField(upload_to='recipes/recipe/')
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Recipe, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug':self.slug})


class AmoutUnit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('wiki.Ingredient', on_delete=DO_NOTHING)
    amount = models.IntegerField()
    unit = models.ForeignKey('AmoutUnit', on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient.name}: {self.recipe.title}'


class RecipeStep(models.Model):
    image = models.ImageField(upload_to='recipes/recipesteps/')
    description = models.TextField(max_length=5000)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
