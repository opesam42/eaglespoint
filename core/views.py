from django.shortcuts import render, redirect
from listing.models import Listings

# Create your views here.
def home(request):
    return render(request, 'core/index.html')


def page_not_found_view(request, exception):
    context = {
        'error_message': 'Sorry, the page you are looking for does not exist.',
    }
    return render(request, 'error_pages/404.html', context, status=404)

def error_page(request):
    return render(request, 'error_pages/error.html', status=403)


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
