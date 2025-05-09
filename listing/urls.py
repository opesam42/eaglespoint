from django.contrib import admin
from django.urls import path
from . import views

app_name = "listing"

urlpatterns = [
    path('search/', views.search_listing, name='search_listing'),
    path('toggle-listing-status/<int:listing_id>/', views.toggle_listing_status, name="toggle_listing_status"),
    path('toggle-favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/', views.favourite_listing, name='favourite_listings'),

    path('get-states/', views.get_states_api, name='get_states')
]
