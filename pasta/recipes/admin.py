from django.contrib import admin
from django.db.models import fields
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(AmoutUnit)
class AmoutUnitAdmin(admin.ModelAdmin):
    pass

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    pass
