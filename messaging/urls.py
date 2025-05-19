from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('send-contact-form/', views.api_create_contact_message, name='send-contact-form'),

]