from django.contrib import admin
from django.urls import path
from . import views

app_name = 'cmscontent'

urlpatterns = [
    path('testimonial/add/', views.create_testimonial, name='create-testimonial'),
    path('testimonial/update/<int:id>/', views.update_testimonial, name='update-testimonial'),
    path('testimonial/delete<int:id>/', views.delete_testimonial, name='delete-testimonial'),

    path('member/create', views.create_team_member, name='create-team-member'),
    path('memeber/update/<int:id>', views.update_team_member, name='update-team-member'),
    path('/member/save-order/', views.save_order_team_member, name='save-order-team-member'),
    path('member/delete/<int:id>', views.delete_team_member, name='delete-member'),

    path('faq/create', views.add_faq, name='create-faq'),
    path('faq/update/<int:id>', views.update_faq, name='update-faq'),
    path('faq/save-order', views.save_order_faqs, name='save-order-faq'),
    path('faq/delete/<int:id>', views.delete_faq, name='delete-faq'),
]
