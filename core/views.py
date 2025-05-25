from django.shortcuts import render, redirect
from listing.models import Listings
from utils.choices import LISTING_TYPE
from cmscontent.models import Testimonial, FAQ

# Create your views here.

# travel page
def home(request):
    testimonials = Testimonial.objects.filter(category='travel').order_by('?')
    return render(request, 'core/index.html', {'testimonials': testimonials})


def page_not_found_view(request, exception):
    context = {
        'error_message': 'Sorry, the page you are looking for does not exist.',
    }
    return render(request, 'error_pages/404.html', context, status=404)

def error_page(request):
    return render(request, 'error_pages/error.html', status=403)


def real_estate_page(request):
    all_listings = Listings.objects.filter(is_listed=True).order_by('-created_at')
    latest_listings = all_listings[:6]
    land_listings = all_listings.filter(listing_type='land')[:6]
    houses_for_sale = all_listings.filter(listing_type='buy')[:6]
    houses_for_rent = all_listings.filter(listing_type='rent')[:6]

    if request.user.is_authenticated:
        user_favourites = Listings.objects.filter(is_listed=True, favourites__user=request.user)
    else:
        user_favourites = []
        
    context = {
        'listings': latest_listings,
        'listing_types': LISTING_TYPE,
        'user_favourites': user_favourites,
        'land_listings': land_listings,
        'houses_for_sale': houses_for_sale,
        'houses_for_rent': houses_for_rent,
    }

    return render(request, 'core/real_estate.html', context)

def about_us_page(request):
    return render(request, 'core/about-us.html')

def contact_page(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    return render(request, 'core/contact.html', {'faqs':faqs })
