from django.contrib import admin
from django.template.defaultfilters import truncatechars
from .models import Cuisine, Menu, Recipe, AmoutUnit, RecipeIngredient, RecipeStep


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 0


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
    exclude = ['slug']
    list_display = ('title', 'slug', 'cuisine', 'menu', 'author', 'is_published',)
    list_filter = ('cuisine', 'menu', 'is_published',)
    search_fields = ('title', 'slug', 'author__email')
    ordering = ('title', 'slug',)
    inlines = [RecipeIngredientInline, RecipeStepInline]

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

    @admin.display(description='рецепт.slug')
    def get_recipe_slug(self, obj):
        return obj.recipe.slug

    @admin.display(description='пользователь')
    def get_author_email(self, obj):
        return obj.recipe.author.email


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('get_short_description', 'recipe', 'get_recipe_slug', 'get_author_email',)
    search_fields = ('description', 'recipe__title', 'recipe__slug', 'recipe__author__email',)
    ordering = ('id',)

    @admin.display(description='описание')
    def get_short_description(self, obj):
        return truncatechars(obj.description, 300)
    
    @admin.display(description='рецепт.slug')
    def get_recipe_slug(self, obj):
        return obj.recipe.slug

    @admin.display(description='пользователь')
    def get_author_email(self, obj):
        return obj.recipe.author.email
