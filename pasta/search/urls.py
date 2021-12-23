from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='search'),
    path('recipes/', views.RecipeSearchListView.as_view(), name='recipe-search'),
    path('ingredients/', views.index, name='ingredient-search'),
    path('instruments/', views.index, name='instrument-search'),
]