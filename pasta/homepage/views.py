from django.http.request import HttpRequest
from django.shortcuts import render
from recipes.models import Recipe
from wiki.models import Ingredient, Instrument
import random, json
from django.db.models import Model


COOKIES_EXPIRE_TIME = 1800
RECIPE_RANDOM_SAMPLE_SIZE = 5
INGREDIENT_RANDOM_SAMPLE_SIZE = 3
INSTRUMENT_RANDOM_SAMPLE_SIZE = 3


def get_random_queryset(
                model_obj: Model, 
                request: HttpRequest, 
                max_age: float, 
                ss: int, 
                get_expired: bool = False, 
                **kwargs
            ):
    model_name = model_obj.__name__.lower()
    qs = model_obj.objects.filter(**kwargs)
    ids, expired = request.get_signed_cookie(f'{model_name}_ids', False, max_age=max_age), False
    if ids is False:
        expired = True
        db_ids = list(qs.values_list('id', flat=True))
        ids = random.sample(db_ids, min(ss, len(db_ids)))
    else:
        ids = json.loads(ids)
    qs = qs.filter(id__in=ids)
    if get_expired:
        return qs, ids, expired
    return qs, ids

def index(request: HttpRequest):
    recipe_qs, recipe_ids, expired = get_random_queryset(
                                        Recipe, 
                                        request, 
                                        COOKIES_EXPIRE_TIME, 
                                        RECIPE_RANDOM_SAMPLE_SIZE, 
                                        get_expired=True, 
                                        is_published=1
                                    )
    ingredient_qs, ingredient_ids = get_random_queryset(
                                        Ingredient, 
                                        request, 
                                        COOKIES_EXPIRE_TIME, 
                                        INGREDIENT_RANDOM_SAMPLE_SIZE
                                    )
    instrument_qs, instrument_ids = get_random_queryset(
                                        Instrument, 
                                        request, 
                                        COOKIES_EXPIRE_TIME, 
                                        INSTRUMENT_RANDOM_SAMPLE_SIZE
                                    )

    favorites = []
    if request.user.is_authenticated:
        favorites = request.user.favorites.all()

    response = render(
        request,
        'index.html',
        context={
            'recipe_list': recipe_qs.select_related('menu', 'cuisine'),
            'ingredient_list': ingredient_qs.select_related('group'),
            'instrument_list': instrument_qs,
            'favorites': favorites,
        }
    )
    if expired:
        response.set_signed_cookie('recipe_ids', recipe_ids)
        response.set_signed_cookie('ingredient_ids', ingredient_ids)
        response.set_signed_cookie('instrument_ids', instrument_ids)
    return response
