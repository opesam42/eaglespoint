from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Listings, ListingImages
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
import os
import json
from django.http import JsonResponse
from utils.choices import STATE_CHOICES

# Create your views here.
def get_states_api(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'states_and_lgas.json')

    with open(file_path, 'r') as f:
        data =json.load(f)
    
    return JsonResponse(data, safe=False)


def search_listing(request):
    listings = Listings.objects.all().order_by('-created_at')

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
    
    paginator = Paginator(listings, 3) #show 20 listing per page
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
        'nigeria_states': Listings.objects.values_list('state', flat=True).order_by('state').distinct()

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