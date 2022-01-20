from django.db import models
from django.urls import reverse
from pytils.translit import slugify

class IngredientGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='wiki/ingredientgroups/', verbose_name='иллюстрация')

    class Meta:
        verbose_name = 'группа ингредиентов'
        verbose_name_plural = 'группы ингредиентов'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('group-ingredients-list', kwargs={'group_slug':self.slug})


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    group = models.ForeignKey('IngredientGroup', on_delete=models.SET_NULL, null=True, verbose_name='группа')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='wiki/ingredients/', verbose_name='иллюстрация')

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'group_slug': self.group.slug, 'slug':self.slug})


class Instrument(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='wiki/instruments/', verbose_name='иллюстрация')

    class Meta:
        verbose_name = 'инструмент'
        verbose_name_plural = 'инструменты'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('instrument-detail', kwargs={'slug':self.slug})
