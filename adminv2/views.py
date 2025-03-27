from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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

            return JsonResponse({"success": True, "message": "Listing added successfully!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
                

            # return redirect('adminv2:listing')
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
    
    form = ListingForm(instance=listingEdit)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listingEdit)
        multiple_images = request.FILES.getlist('multiple_images[]')
        
        if form.is_valid():
            listing = form.save(commit=False)

            # Keep existing cover image if no new file is uploaded
            if "cover_image" not in request.FILES:
                listing.cover_image = listing.cover_image  # Keep old image
            
            listing.save()

            form.save_m2m() #save features

            # Get the list of existing images
            existing_images = ListingImages.objects.filter(listing_id=property_id)

            # Collect the names of existing images
            existing_image_names = {img.image.name for img in existing_images}
            print(existing_image_names)

            # Get the list of new images being uploaded
            new_image_names = {image.name for image in multiple_images}

            # Remove images that are not in the new image list
            for image in existing_images:
                if image.image.name not in new_image_names:
                    # Optionally, you can add logic here to delete the image from storage
                    image.delete()

            # Upload new images that are not already associated with the listing
            for image in multiple_images:
                if image.name not in existing_image_names:
                    ListingImages.objects.create(listing=listing, image=image)
            
            #END MULTIMAGE PROCESSING    
                

            # return redirect('adminv2:listing')
            return JsonResponse({"message": "Listing updated successfully"})
        
        else:
            return JsonResponse({"error": "Form is invalid", "errors": form.errors}, status=400)
        

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