from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate-account'),
    path('profile/change_personal_info/', views.change_user_personal_info, name='profile-info-change'),
    path('profile/password_change/', views.password_change, name='password-change'),
    path('profile/favorites/', views.FavoritesListView.as_view(), name='profile-favorites'),
    path('profile/myrecipes/', views.MyRecipesListView.as_view(), name='profile-myrecipes'),
]