from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = 'user'

urlpatterns = [
    path('register/', views.sign_up, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('agent/register/', views.agent_form, name='agent-register-form'),
    path('settings/', views.user_settings, name='settings'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate'),
    path('resend-activation/<uid>', views.resend_activation_token, name='resend_activation'),
    path('unblock-account/', views.unblock_account_page, name='unblock-account-page'),
    path('send-unblock-request/', views.unblock_request, name='send-unblock-request'),

    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', success_url=reverse_lazy('user:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]
