from dataclasses import field
from django import forms
from django.contrib import admin
from django.template.defaultfilters import truncatechars
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep
from .views import COOKING_TIME_INITIAL_DATA

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 0


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'cooking_time': forms.TimeInput(attrs={'type': 'time'})
        }


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    exclude = ['slug']
    list_display = ('title', 'slug', 'cuisine', 'menu', 'author', 'creation_date', 'is_published',)
    list_filter = ('cuisine', 'menu', 'creation_date', 'is_published',)
    search_fields = ('title', 'slug', 'author__email')
    ordering = ('title', 'slug', 'creation_date',)
    inlines = [RecipeIngredientInline, RecipeStepInline]

    def get_changeform_initial_data(self, request):
        return {'cooking_time': COOKING_TIME_INITIAL_DATA}


@admin.register(AmoutUnit)
class AmoutUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'need_amount',)
    list_filter = ('need_amount',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'unit', 'recipe', 'get_recipe_slug', 'get_author_email',)
    search_fields = ('ingredient__name', 'recipe__title', 'recipe__slug', 'recipe__author__email',)
    ordering = ('ingredient',)

    @admin.display(description='????????????.slug')
    def get_recipe_slug(self, obj):
        return obj.recipe.slug

    @admin.display(description='????????????????????????')
    def get_author_email(self, obj):
        return obj.recipe.author.email


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('get_short_description', 'recipe', 'get_recipe_slug', 'get_author_email',)
    search_fields = ('description', 'recipe__title', 'recipe__slug', 'recipe__author__email',)
    ordering = ('id',)

    @admin.display(description='????????????????')
    def get_short_description(self, obj):
        return truncatechars(obj.description, 300)
    
    @admin.display(description='????????????.slug')
    def get_recipe_slug(self, obj):
        return obj.recipe.slug

    @admin.display(description='????????????????????????')
    def get_author_email(self, obj):
        return obj.recipe.author.email
