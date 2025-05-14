from django.contrib import admin
from django.urls import path
from . import views

app_name = "listing"

urlpatterns = [
    path('search/', views.search_listing, name='search_listing'),
    path('lands', views.search_listing, {'default_listing_type': 'land'}, name='land_listings'),
    path('properties-for-sale', views.search_listing, {'default_listing_type': 'buy'}, name='properties_for_sale'),
    path('properties-for-rent', views.search_listing, {'default_listing_type': 'rent'}, name='properties_for_rent'),
    path('toggle-listing-status/<int:listing_id>/', views.toggle_listing_status, name="toggle_listing_status"),
    path('toggle-favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/', views.favourite_listing, name='favourite_listings'),

    path('get-states/', views.get_states_api, name='get_states')
]
