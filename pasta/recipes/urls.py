from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recipes'),
    path('<slug:slug>', views.index, name='recipe-detail')
]