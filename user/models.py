from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
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
    is_block = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user_role == 'agent':
            # Create or update the Agents record for this user
            Agent.objects.get_or_create(user=self)
        else:
            # If not an agent, remove from Agents table if exists
            Agent.objects.filter(user=self).delete()

    def __str__(self):
        return self.email
 
class Agent(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    renewal_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Agent {self.user.first_name} {self.user.last_name}"

class PasswordReset(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)