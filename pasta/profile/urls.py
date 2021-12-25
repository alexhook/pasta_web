from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='profile'),
    path('info_update/', views.index, name='profile-info-update'),
    path('info_update_done/', views.index, name='profile-info-update-done'),
    path('password_reset/', views.index, name='profile-password-reset'),
    path('password_reset_done/', views.index, name='profile-password-reset-done'),
    path('favorites/', views.index, name='profile-favorites'),
    path('myrecipes/', views.index, name='profile-myrecipes'),
]