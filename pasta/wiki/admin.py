from django.contrib import admin
from django.contrib.admin.decorators import display
from .models import IngredientGroup, Ingredient, Instrument

@admin.register(IngredientGroup)
class IngredientGroupAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ('name', 'get_ingredient_count',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)

    @admin.display(description='Количество ингредиентов')
    def get_ingredient_count(self, obj):
        return Ingredient.objects.filter(group=obj).count()

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ('name', 'group',)
    list_filter = ('group',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)
