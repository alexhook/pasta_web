from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='search'),
    path('recipes/', views.RecipeSearchListView.as_view(), name='recipe-search'),
    path('ingredients/', views.IngredientSearchListView.as_view(), name='ingredient-search'),
    path('instruments/', views.InstrumentSearchListView.as_view(), name='instrument-search'),
]