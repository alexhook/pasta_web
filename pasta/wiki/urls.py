from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='wiki'),
    path('ingredients/', views.IngredientGroupListView.as_view(), name='ingredient-groups-list'),
    path('ingredients/<slug:group_slug>/', views.IngredientListView.as_view(), name='group-ingredients-list'),
    path('ingredients/<slug:group_slug>/<slug:slug>', views.IngredientDetailView.as_view(), name='ingredient-detail'),
    path('instruments/', views.InstrumentListView.as_view(), name='instruments-list'),
    path('instruments/<slug:slug>/', views.InstrumentDetailView.as_view(), name='instrument-detail'),
]