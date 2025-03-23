from django.contrib import admin
from django.urls import path
from . import views

app_name = "listing"

urlpatterns = [
    path('search/', views.search_listing, name='search_listing'),
    path('property/<int:property_id>/', views.listing_details, name="property_details" ),

    path('get-states/', views.get_states_api, name='get_states')
]
