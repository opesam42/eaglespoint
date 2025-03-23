from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Listings, ListingImages
from django.db.models import Q
from django.conf import settings
import os
import json
from django.http import JsonResponse

# Create your views here.
def get_states_api(request):
    file_path = os.path.join(settings.BASE_DIR, 'listing', 'data', 'states_and_lgas.json')

    with open(file_path, 'r') as f:
        data =json.load(f)
    
    return JsonResponse(data, safe=False)

def search_listing(request):
    search_query = request.GET.get('search_query', '').strip()  # Get search query from GET request
    if search_query:
        listings = Listings.objects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(lga__icontains=search_query) |
            Q(state__icontains=search_query)
        )

        #handle filters
        listing_type = request.GET.get('listing_type', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        lga = request.GET.get('lga', '')
        state = request.GET.get('state', '')

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

        # results = Listings.objects.filter(title__icontains=search_query) if search_query else []  # Filter results

    context = {
        'results': listings,
        'search_query': search_query,
        'listing_type': listing_type,
        'min_price': min_price,
        'max_price': max_price,
        'lga': lga,
        'state': state,
    }
    
    return render(request, 'listing/search.html', context)


def listing_details(request, property_id):
    property = get_object_or_404(Listings, id=property_id)
    property_images = ListingImages.objects.filter(listing_id=property_id).values()
    features = property.features.all()

    context = {
        'listing': property,
        'listing_images': property_images,
        'features': features,
    }

    return render(request, "listing/details.html", context)