from django.db import models

class IngredientGroup(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='wiki/ingredientgroups/')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey('IngredientGroup', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='wiki/ingredients/')
    
    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='wiki/instruments/')

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
