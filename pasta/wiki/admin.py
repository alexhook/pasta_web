from django.contrib import admin
from .models import IngredientGroup, Ingredient, Instrument

@admin.register(IngredientGroup)
class IngredientGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
