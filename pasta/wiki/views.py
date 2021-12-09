from django.shortcuts import render
from django.http.request import HttpRequest
from .models import IngredientGroup

def index(request: HttpRequest):
    groups = IngredientGroup.objects.all()
    return render(
        request,
        'wiki.html',
        context={'groups': groups}
    )
