from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('create/', views.recipe_create_form, name='recipe-create'),
    path('show/<slug:slug>', views.RecipeDetailView.as_view(), name='recipe-detail'),
]