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
    path('listing-search/<str:search_query>', views.search_listing, name="search_listing"),
    path('listing-search/', views.search_listing, name='search_listing_all'),
    path('listing/delete/<int:listing_id>', views.delete_listing, name="delete-listing"),

    path('user/', views.user_control_page, name="user-control-page"),
    path('get-users/', views.get_users, name='get-users'),
    path('user/toggle-admin/<int:user_id>', views.toggle_admin, name="toggle-admin"),
    path('user/info/<int:user_id>', views.user_info, name="user-info"),

    path('message', views.message_page, name="message-page"),
    path('get-messages/', views.get_messages, name="get-messages"),
    path('get-messages/<int:message_id>/', views.get_messages, name="get-messages"),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete-message'),
]
