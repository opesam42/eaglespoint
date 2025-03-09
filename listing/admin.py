from django.contrib import admin
from .models import Listings, ListingImages

# Register your models here.
admin.site.register(Listings)
admin.site.register(ListingImages)