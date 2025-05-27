from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.view_all_blogs, name='home'), 
    # path('create/', views.blog_create, name='create-blog'),
    path('<str:slug>', views.view_specific_blog, name='article'),
    
]
