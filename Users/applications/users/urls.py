from django.contrib import admin
from django.urls import path
from .views import UserRegisterView, LoginUser, LogoutView, UpdatePassword, CodeVerificationView

app_name = "users_app"

urlpatterns = [
    path(
        'register/', 
        UserRegisterView.as_view(),
        name='user-register'
        ),
    path(
        'login/', 
        LoginUser.as_view(),
        name='user-login'
        ),
    path(
        'logout/', 
        LogoutView.as_view(),
        name='user-logout'
        ),
    path(
        'update/', 
        UpdatePassword.as_view(),
        name='user-update'
        ),
    path(
        'user-verification/<pk>/', 
        CodeVerificationView.as_view(),
        name='user-verification'
        ),
]