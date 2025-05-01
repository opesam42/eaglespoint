from django.contrib import admin
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('real-estate/', views.real_estate_page, name='real_estate'),
    path('about/', views.about_us_page, name='about'),
    path('contact/', views.contact_page, name='contact'),

    path('error-page', views.error_page, name='error_page')
]
