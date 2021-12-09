from django.contrib import admin
from .models import IngredientGroup, Ingredient, Instrument, Cuisine, Menu

@admin.register(IngredientGroup)
class IngredientGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    pass

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass
