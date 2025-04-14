from django.shortcuts import render, redirect
from listing.models import Listings

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def real_estate_page(request):
    listings = Listings.objects.all().order_by('-created_at')[:6]
    if request.user.is_authenticated:
        user_favourites = Listings.objects.filter(favourites__user=request.user)
    else:
        user_favourites = []
    context = {
        'listings': listings,
        'user_favourites': user_favourites,
    }

    return render(request, 'core/real_estate.html', context)

def about_us_page(request):
    return render(request, 'core/about-us.html')

def contact_page(request):
    return render(request, 'core/contact.html')
