from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):

    USER_TYPE = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    )

    username = None #remove username, I want to use email as unique identifier
    email = models.EmailField(_("email address"), unique=True)
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15)
    user_role = models.CharField(max_length=10, choices=USER_TYPE, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email