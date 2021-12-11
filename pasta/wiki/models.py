from django.db import models
from django.urls import reverse

class IngredientGroup(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='wiki/ingredientgroups/')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group-ingredients-list', kwargs={'group':self.slug})


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    group = models.ForeignKey('IngredientGroup', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='wiki/ingredients/')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'group': self.group.slug, 'slug':self.slug})


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='wiki/instruments/')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('instrument-detail', kwargs={'slug':self.slug})
