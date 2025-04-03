from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'user'

urlpatterns = [
    path('register/', views.sign_up, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate'),
    path('resend-activation/<uid>', views.resend_activation_token, name='resend_activation'),

    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]
