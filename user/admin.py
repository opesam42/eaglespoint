from django.contrib import admin
from .models import CustomUser, Agent
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Agent)