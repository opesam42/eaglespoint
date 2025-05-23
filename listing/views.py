from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Listings, ListingImages, Favourites
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
import os
from django.urls import reverse
from urllib.parse import quote
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

@login_required
def favourite_listing(request):
    # TODO: will allow all to show irrespective of the "is_listed" state but the one with the "is_listed=False" would be made disabled
    user_favourites = Listings.objects.filter(is_listed=True, favourites__user=request.user)
    context = {
        'listings': user_favourites,
        'user_favourites': user_favourites,
        }
    return render(request, 'listing/favourite.html', context)

def search_listing(request, default_listing_type = None):
    # listings = Listings.objects.filter(is_listed=True).order_by('-created_at')
    
    context_type = request.GET.get('context', 'user')
    selected_sort = request.GET.get('selected_sort', '')
    sort_options = {
        'date_desc': '-created_at',
        'date_asc': 'created_at',
        'price_desc': '-price',
        'price_asc': 'price'
    }

    order_by_field = sort_options.get(selected_sort, '-created_at') #default option '-created_at'
    if context_type == 'user':
        listings = Listings.objects.filter(is_listed=True).order_by(order_by_field)
    else:
        listings = Listings.objects.all().order_by(order_by_field)
    
    if request.user.is_authenticated:
        user_favourites = Listings.objects.filter(favourites__user=request.user)
    else:
        user_favourites = []

    search_query = request.GET.get('search_query', '').strip()  # Get search query from GET request
    if search_query:
        search_words = search_query.split() #split search string to individual words
        
        query = Q()
        for word in search_words:
            query |=  Q(title__icontains=word) | Q(description__icontains=word) | Q(lga__icontains=word) | Q(state__icontains=word)
        listings = listings.filter(query)

    #handle filters
    listing_type = request.GET.get('listing_type', '') or default_listing_type
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
    total_pages = listings.paginator.num_pages
    current_page = listings.number
    
    #handle ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if context_type == 'admin':
            template = 'adminv2/listing/partials/listing-items.html'
            # data = []
            # for listing in listings:
            #     data.append({
            #         'id': listing.id,
            #         'title': listing.title,
            #         'description': listing.description,
            #         'price': listing.price,
            #         'state': listing.state,
            #         'lga': listing.lga,
            #         'listing_type': listing.listing_type,
            #         'created_at': listing.created_at.strftime('%Y-%m-%d'),
            #     })
            #     return JsonResponse({'listings': data})
        else:
            template = 'listing/partials/listing-items.html'
            
        return render(request, template, {
            'results': listings,
            'user_favourites': user_favourites,
            'has_previous': listings.has_previous(),
            'has_next': listings.has_next(),
            'next_page': listings.next_page_number() if listings.has_next() else None,
            'previous_page': listings.previous_page_number() if listings.has_previous() else None,
            'total_pages': total_pages,
            'current_page': current_page,
            })

    context = {
        'results': listings,
        'search_query': search_query,
        'selected_sort': selected_sort,
        'listing_type': listing_type,
        'min_price': min_price,
        'max_price': max_price,
        'lga': lga,
        'selectedState': state,
        'nigeria_states': Listings.objects.values_list('state', flat=True).order_by('state').distinct(),
        'user_favourites': user_favourites,
    }
    
    return render(request, 'listing/search.html', context)


def get_listing_context(request, property):
    property_images = ListingImages.objects.filter(listing_id=property.id).values()
    features = property.features.all()

    property_url = reverse('core:property_details_by_slug', kwargs={'slug': property.slug})
    full_url = property_url if property.slug else reverse('core:property_details_by_id', kwargs={'property_id': property.id})
    full_url = request.build_absolute_uri(full_url)

    whatsapp_message = (
        f"Good day Eaglespoint, I am interested in the following property:\n"
        f"*{property.title}*\n"
        f"Link: {full_url}\n"
        f"Please provide more details. Thank you!"
    )
    encoded_message = quote(whatsapp_message)
    whatsapp_number = "+2348086818881"
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

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


    return {
        'listing': property,
        'listing_images': signed_image_urls,
        'features': features,
        'is_favourite': is_favourite,
        'whatsapp_link': whatsapp_link,
    }

   
def listing_details_by_id(request, property_id):
    property = get_object_or_404(Listings, id=property_id)
    if property.slug:
        return redirect('core:property_details_by_slug', slug=property.slug)
    context = get_listing_context(request, property)
    return render(request, "listing/details.html", context)

def listing_details_by_slug(request, slug):
    property = get_object_or_404(Listings, slug=slug)
    context = get_listing_context(request, property)
    return render(request, "listing/details.html", context)



def toggle_favourite(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Anonymous user'}, status=401)

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
