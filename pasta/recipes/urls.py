from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('create/', views.recipe_create_form, name='recipe-create'),
    path('show/<slug:slug>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('edit/<slug:slug>', views.recipe_edit_form, name='recipe-edit'),
    path('remove/<slug:slug>', views.RecipeDeleteView.as_view(), name='recipe-remove'),
    path('publish/<slug:slug>', views.change_recipe_publish, name='recipe-publish'),
]