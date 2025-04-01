from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.sign_up, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate'),
    path('resend-activation/<uid>', views.resend_activation_token, name='resend_activation')
]
