from django.contrib import admin
from django.urls import path
from . import views
from listing.views import listing_details_by_id, listing_details_by_slug

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('real-estate/', views.real_estate_page, name='real_estate'),
    path('about/', views.about_us_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('property/<int:property_id>/', listing_details_by_id, name='property_details_by_id'),
    path('property/<slug:slug>/', listing_details_by_slug, name='property_details_by_slug'),

    path('error-page', views.error_page, name='error_page')
]
