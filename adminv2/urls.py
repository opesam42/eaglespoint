from django.contrib import admin
from django.urls import path
from . import views

app_name = 'adminv2'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listing/', views.listing, name="listing"),
    path('listing/add/', views.add_listing, name="add_listing"),
    path('listing/edit/<int:property_id>', views.edit_listing, name="edit-listing"),

    path('listing/delete/<int:listing_id>', views.delete_listing, name="delete-listing"),
]
