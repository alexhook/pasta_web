from django.http.request import HttpRequest
from django.shortcuts import render
from recipes.models import Recipe
import random, json


COOKIES_EXPIRE_TIME = 30
RECIPE_RANDOM_SAMPLE_SIZE = 1


def index(request: HttpRequest):
    recipe_random_ids = request.get_signed_cookie('recipe_random_ids', False, max_age=COOKIES_EXPIRE_TIME)
    recipe_queryset = Recipe.objects.filter(is_published=1)
    if recipe_random_ids is False:
        recipe_ids_list = list(recipe_queryset.values_list('id', flat=True))
        recipe_random_ids = random.sample(recipe_ids_list, min(RECIPE_RANDOM_SAMPLE_SIZE, len(recipe_ids_list)))
    else:
        recipe_random_ids = json.loads(recipe_random_ids)
    recipe_random_queryset = recipe_queryset.filter(id__in=recipe_random_ids).select_related('menu', 'cuisine')
    response = render(
        request,
        'index.html',
        context={
            'recipe_list': recipe_random_queryset,
        }
    )
    response.set_signed_cookie('recipe_random_ids', recipe_random_ids)
    return response
