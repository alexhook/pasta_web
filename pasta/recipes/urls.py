from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('<slug:slug>', views.RecipeDetailView.as_view(), name='recipe-detail')
]