from django.contrib import admin
from django.urls import path
from . import views

app_name = 'cmscontent'

urlpatterns = [
    path('testimonial/add/', views.create_testimonial, name='create-testimonial'),
    path('testimonial/update/<int:id>/', views.update_testimonial, name='update-testimonial'),
    path('testimonial/delete<int:id>/', views.delete_testimonial, name='delete-testimonial')
]
