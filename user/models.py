from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


def user_directory_path(instance, filename):
    return f'user/user_{instance.id}/{filename}'

# Create your models here.
class CustomUser(AbstractUser):

    USER_TYPE = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    )

    username = None #remove username, I want to use email as unique identifier
    email = models.EmailField(_("email address"), unique=True)
    # TO-DO: If you is important, make phone number field compulsory
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    user_role = models.CharField(max_length=10, choices=USER_TYPE, default='customer')
    profileImage = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email