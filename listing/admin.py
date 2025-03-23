from django.contrib import admin
from .models import Listings, ListingImages, Feature

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')  # Show feature ID and name in the list view
    search_fields = ('name',)  # Allow searching by feature name
    ordering = ('name',)  # Order features alphabetically

@admin.register(Listings)
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing_type', 'price', 'state', 'created_at')
    search_fields = ('title', 'state', 'listing_type')
    list_filter = ('listing_type', 'state', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ('features',)  # Allows selecting multiple features in a better UI

admin.site.register(ListingImages)
