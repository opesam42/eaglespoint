from django.shortcuts import render, redirect
from listing.models import Listings

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def real_estate_page(request):
    return render(request, 'core/real_estate.html')

def about_us_page(request):
    return render(request, 'core/about-us.html')

def contact_page(request):
    return render(request, 'core/contact.html')
