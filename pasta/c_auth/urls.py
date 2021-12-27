from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.index, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate-account'),
#     path('info/', views.index, name='profile-info'),
#     path('password_reset/', views.index, name='profile-password-reset'),
#     path('favorites/', views.index, name='profile-favorites'),
#     path('myrecipes/', views.index, name='profile-myrecipes'),
]