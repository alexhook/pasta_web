from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class WikiSection(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    image = models.ImageField(upload_to='wiki/wikisections/', verbose_name='Иллюстрация')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
    
    def __str__(self):
        return self.name


class IngredientGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='wiki/ingredientgroups/', verbose_name='Иллюстрация')

    class Meta:
        verbose_name = 'Группа ингредиентов'
        verbose_name_plural = 'Группы ингредиентов'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.slug == slug:
            self.slug = slug
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('group-ingredients-list', kwargs={'group_slug':self.slug})


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    group = models.ForeignKey('IngredientGroup', on_delete=models.SET_NULL, null=True, verbose_name='Группа')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='wiki/ingredients/', verbose_name='Иллюстрация')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.slug == slug:
            self.slug = slug
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'group_slug': self.group.slug, 'slug':self.slug})


class Instrument(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='wiki/instruments/', verbose_name='Иллюстрация')

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.slug == slug:
            self.slug = slug
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('instrument-detail', kwargs={'slug':self.slug})
