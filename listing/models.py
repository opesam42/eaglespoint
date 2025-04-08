from django.db import models
from django.conf import settings
from utils.choices import STATE_CHOICES, LISTING_TYPE

# Create your models here.

class Feature(models.Model):
    """ 
    Table for individual features (e.g., Swimming Pool, Parking Space) 
    """
    name = models.CharField(max_length=50, unique=True)
    icon = models.TextField(null=True, blank=True) #accept svg icons in code format not files
    """ 
    I am using Google Material fonts https://fonts.google.com/icons?selected=Material+Icons:wifi:&icon.query=wifi&icon.size=32&icon.color=%23%23101828&icon.platform=web
    size: 32 x 32
    color: #101828  
    """
    
    

    class Meta:
        verbose_name_plural = "Features"

    def __str__(self):
        return f"{self.name}"

class Listings(models.Model):
    """ 
    MODEL CLASS FOR LISTINGS TABLE AND SCHEMA
    """

    # core details
    title = models.CharField(max_length=40, blank=False, null=False)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=False, null=False)
    cover_image = models.ImageField(upload_to='listing-cover/', blank=False, null=False)
    size = models.IntegerField(blank=True, null=True) # represent size in square meter for land and units for rented/sold housing 

    # address
    street_address = models.CharField(max_length=100, blank=False, null=False)
    lga = models.CharField(max_length=30, blank=False, null=False)
    # state = models.CharField(max_length=30, blank=False, null=False)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, blank=False, null=False)
    country = models.CharField(max_length=30, default="Nigeria", blank=False, null=False)

    features = models.ManyToManyField(Feature, related_name='listings', blank=True)
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_listed = models.BooleanField(default=True)

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
    
class Favourites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listings', on_delete=models.CASCADE, related_name='favourites')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name_plural = "Favourite Listings"
    
    def __str__(self):
        return f"{self.user.username} loves {self.Listing.title}"