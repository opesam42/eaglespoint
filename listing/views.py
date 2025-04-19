from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Listings, ListingImages, Favourites
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
import os
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from utils.role_check import is_admin
from utils.choices import STATE_CHOICES
from utils.storage import get_signed_b2_url

# Create your views here.
def get_states_api(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'states_and_lgas.json')

    with open(file_path, 'r') as f:
        data =json.load(f)
    
    return JsonResponse(data, safe=False)

def favourite_listing(request):
    listings = Listings.objects.all().order_by('-created_at')
    user_favourites = Listings.objects.filter(favourites__user=request.user)
    context = {
        'listings': user_favourites,
        'user_favourites': user_favourites,
        }
    return render(request, 'listing/favourite.html', context)

def search_listing(request):
    listings = Listings.objects.all().order_by('-created_at')
    user_favourites = Listings.objects.filter(favourites__user=request.user)

    search_query = request.GET.get('search_query', '').strip()  # Get search query from GET request
    if search_query:
        search_words = search_query.split() #split search string to individual words
        
        query = Q()
        for word in search_words:
            query |=  Q(title__icontains=word) | Q(description__icontains=word) | Q(lga__icontains=word) | Q(state__icontains=word)
        listings = listings.filter(query)

    #handle filters
    listing_type = request.GET.get('listing_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    lga = request.GET.get('lga', '')
    state = request.GET.get('state', '')
    page_number = request.GET.get('page')

    if listing_type:
        listings = listings.filter(listing_type=listing_type)

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    if lga:
        listings = listings.filter(lga__icontains=lga)

    if state:
        listings = listings.filter(state__icontains=state)
    
    paginator = Paginator(listings, 20) #show 20 listing per page
    listings = paginator.get_page(page_number)
    
    #handle ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'listing/partials/listing-items.html', {
            'results': listings,
            'has_next': listings.has_next(),
            'next_page': listings.next_page_number() if listings.has_next() else None,
            })

    context = {
        'results': listings,
        'search_query': search_query,
        'listing_type': listing_type,
        'min_price': min_price,
        'max_price': max_price,
        'lga': lga,
        'selectedState': state,
        'nigeria_states': Listings.objects.values_list('state', flat=True).order_by('state').distinct(),
        'user_favourites': user_favourites,
    }
    
    return render(request, 'listing/search.html', context)


def listing_details(request, property_id):
    property = get_object_or_404(Listings, id=property_id)
    property_images = ListingImages.objects.filter(listing_id=property_id).values()
    features = property.features.all()

    user_favourite = None
    if request.user.is_authenticated:
        user_favourites = Listings.objects.filter(favourites__user=request.user)
        def check_if_favourite():
            if property in user_favourites:
                print('yeah')
                return True
            else:
                print('nay')
                return False
        is_favourite = check_if_favourite()
    else:
        is_favourite = None
        # check_if_favourite()

    # Generate signed URLs for images from backblaze
    signed_image_urls = []
    for image in property_images:
        image_url = get_signed_b2_url(image['image']) 
        signed_image_urls.append(image_url)


    context = {
        'listing': property,
        'listing_images': signed_image_urls,
        'features': features,
        'is_favourite': is_favourite
    }

    return render(request, "listing/details.html", context)


@login_required
def toggle_favourite(request):
    listing_id = request.POST.get("product_id")
    listing = Listings.objects.get(id=listing_id)
    favourite, created = Favourites.objects.get_or_create(user=request.user, listing=listing)

    if not created:
        favourite.delete()
        is_favourite = False
    else:
        is_favourite = True

    return JsonResponse({'is_favourite': is_favourite})


@user_passes_test(is_admin)
def toggle_listing_status(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)

    if request.method == "POST":
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if listing.is_listed == False:
                listing.is_listed = True
            else:
                listing.is_listed = False
            
            listing.save()

            return JsonResponse({
                "success": True,
                "is_listed": listing.is_listed,
                "message": f'Listing status of {listing.title} has been changed to {listing.is_listed}',
            })
    return JsonResponse({
        "success": False,
        "message": "Invalid request",
    }, status=400)
