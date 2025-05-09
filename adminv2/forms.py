from django import forms
from listing.models import Listings, Feature

class ListingForm(forms.ModelForm):
    
    class Meta:
        model = Listings
        fields = ['title', 'listing_type', 'description', 'price', 'cover_image', 'size', 'street_address', 'lga', 'state', 'features', 'slug', 'keywords']