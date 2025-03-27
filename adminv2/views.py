from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ListingForm
from listing.models import Listings, Feature, ListingImages
from utils.choices import LISTING_TYPE, STATE_CHOICES
from utils.role_check import is_admin

# Create your views here.
@user_passes_test(is_admin)
def dashboard(request):
    # print(f"Logged-in user: {request.user.email}, Role: {request.user.user_role}")
    return render(request, 'adminv2/dashboard.html')

@user_passes_test(is_admin)
def listing(request):
    listings = Listings.objects.all()
    

    return render(request, 'adminv2/listing/listing.html', {'results': listings})

@user_passes_test(is_admin)
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)

    if request.method == "POST":
        listing.delete()
        return redirect('adminv2:listing')
    
    return redirect('adminv2:listing')

@user_passes_test(is_admin)
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        multiple_images = request.FILES.getlist('multiple_images[]')
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.posted_by = request.user
            listing.save()

            form.save_m2m() #save features

            for image in multiple_images:
                ListingImages.objects.create(listing=listing, image=image)
                

            return redirect('adminv2:listing')
    else:
        form = ListingForm()

    context = {
        'form': form,
        'listing_types': LISTING_TYPE,
        'nigeria_states': STATE_CHOICES,
        'features': Feature.objects.all(),
    }

    return render(request, 'adminv2/listing/add.html', context)



@user_passes_test(is_admin)
def edit_listing(request, property_id):
    
    listingEdit = get_object_or_404(Listings, id=property_id)
    
    listingImages = list(ListingImages.objects.filter(listing_id=property_id).values_list('image', flat=True))
    listingImagesJson =  mark_safe(json.dumps(listingImages)) #convert to json string in json format
    listingImagesList = json.loads(listingImagesJson) #convert back to list
    listingImagesJson2 = [f"/media/{image}" for image in listingImagesList]
    listingImageArray = mark_safe(json.dumps(listingImagesJson2).replace('"', "'")) #replace double quote with single for it to be accepted by alpine js
    

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        multiple_images = request.FILES.getlist('multiple_images[]')
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.posted_by = request.user
            listing.save()

            form.save_m2m() #save features

            for image in multiple_images:
                ListingImages.objects.create(listing=listing, image=image)
                

            return redirect('adminv2:listing')
    else:
        form = ListingForm()

    context = {
        'form': form,
        'listing_types': LISTING_TYPE,
        'nigeria_states': STATE_CHOICES,
        'features': Feature.objects.all(),

        'listing': listingEdit,
        'listing_features': list(listingEdit.features.values_list('id', flat=True)),
        'listing_images': listingImageArray
    }

    return render(request, 'adminv2/listing/edit.html', context)