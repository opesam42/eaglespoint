from django.db import models
from django.conf import settings

# Create your models here.

class Listings(models.Model):
    """ 
    MODEL CLASS FOR LISTINGS TABLE AND SCHEMA
    """
    LISTING_TYPE = (
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('land', 'Land'),
    )
    # core details
    title = models.CharField(max_length=40, blank=False, null=False)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=False, null=False)
    cover_image = models.ImageField(upload_to='listing-cover/', blank=False, null=False)
    units = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)

    # address
    street_address = models.CharField(max_length=100, blank=False, null=False)
    lga = models.CharField(max_length=30, blank=False, null=False)
    state = models.CharField(max_length=30, blank=False, null=False)
    country = models.CharField(max_length=30, blank=False, null=False)

    features = models.JSONField(blank=True, null=True)
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Listings"

    def __str__(self):
        return f"{self.listing_type} - {self.title}" 
    

class ListingImages(models.Model):
    """ 
    Table for mapping images to their respective listings 
    """
    listing = models.ForeignKey(Listings, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing-images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Listing Images"

    def __str__(self):
        return f"Image for {self.listing.title}"