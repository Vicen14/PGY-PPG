from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='funcionalidades/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='funcionalidades/recuperar.html'), name='password_reset'),
    ]