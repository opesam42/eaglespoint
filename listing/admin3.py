from django.contrib import admin
from .models import Listings, ListingImages

@admin.register(Listings)
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing_type', 'price', 'state', 'created_at')
    search_fields = ('title', 'state', 'listing_type')
    list_filter = ('listing_type', 'state', 'created_at')
    ordering = ('-created_at',)
    

admin.site.register(ListingImages)
