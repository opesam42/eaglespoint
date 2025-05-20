from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.views.decorators.http import require_POST
from .forms import ListingForm
from listing.models import Listings, Feature, ListingImages
from utils.choices import LISTING_TYPE, STATE_CHOICES
from utils.role_check import is_admin, admin_only
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from listing.models import Listings
from utils.storage import delete_cover_image_folder, get_signed_b2_url, BackBlazeAPI
from messaging.models import ContactMessage

User = get_user_model()


# Create your views here.
@admin_only
def dashboard(request):
    users_count = User.objects.count()
    listings_count = Listings.objects.count()
    context = {
        'users_count': users_count,
        'listings_count': listings_count,
    }

    return render(request, 'adminv2/dashboard.html', context)

@admin_only
def listing(request):
    listings = Listings.objects.all()
    nigeria_states = Listings.objects.values_list('state', flat=True).order_by('state').distinct()
    return render(request, 'adminv2/listing/listing.html', {
        'results': listings,
        'nigeria_states': nigeria_states,
    })


@admin_only
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)

    if request.method == "POST":
        listing.delete()
        listing_media_dir = f'listing-images/listing_{listing_id}/'
        print(listing_id)
        try:
            backblaze = BackBlazeAPI()
            backblaze.delete_files_with_prefix(listing_media_dir)
        except Exception as e:
            print(f'Backblaze error: {e}')
        return redirect('adminv2:listing')
    
    return redirect('adminv2:listing')


@admin_only
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        cover_image = request.FILES.get('cover_image')
        multiple_images = request.FILES.getlist('multiple_images[]')
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.posted_by = request.user
            listing.save()
            #i save cover image here so as to take the id of the instance of listing created
            if cover_image:
                listing.cover_image = cover_image
                listing.save()

            form.save_m2m() #save features

            for image in multiple_images:
                ListingImages.objects.create(listing=listing, image=image)

            return JsonResponse({
                "success": True, 
                "message": "Property added successfully!",
                "listing_id": listing.id,
            })
        
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



@admin_only
def edit_listing(request, property_id):
    
    listingEdit = get_object_or_404(Listings, id=property_id)
    
    # listingImages = [f"/media/{image}" for image in ListingImages.objects.filter(listing_id=property_id).values_list('image', flat=True)]
    # listingImageArray = mark_safe(json.dumps(listingImages).replace('"', "'"))

    property_images = ListingImages.objects.filter(listing_id=property_id).values_list('image', flat=True)
    signed_image_urls = [get_signed_b2_url(img) for img in property_images]
    listingImageArray = mark_safe(json.dumps(signed_image_urls))
    
    
    form = ListingForm(instance=listingEdit)

    if request.method == "POST":
        old_cover_image = listingEdit.cover_image
        form = ListingForm(request.POST, request.FILES, instance=listingEdit)
        multiple_images = request.FILES.getlist('multiple_images[]')
        
        if form.is_valid():
            listing = form.save(commit=False)

            # Keep existing cover image if no new file is uploaded
            if "cover_image" in request.FILES:
                if old_cover_image:
                    # to delete the file
                    try:
                        backblaze = BackBlazeAPI()
                        backblaze.delete_files_with_prefix(old_cover_image.name)
                    except Exception as e:
                        print(f'Backblaze error: {e}')
                    
                # delete_cover_image_folder(listing.id)
                listing.cover_image = request.FILES["cover_image"]
            
            form.save()

            # if "cover_image" in request.FILES:
            #     print(f"Cover image uploaded: {request.FILES['cover_image']}")
            #     listing.cover_image = request.FILES["cover_image"]
            #     listing.save()
                
            #     if listing.cover_image:
            #         print(f"Old cover image: {listing.cover_image}")
            #         listing.cover_image.delete(save=False)
    
            #     listing.save()

            form.save_m2m() #save features
            
            # Get the list of existing images
            existing_images = ListingImages.objects.filter(listing_id=property_id)

            for img in existing_images:
                try:
                    backblaze = BackBlazeAPI()
                    backblaze.delete_files_with_prefix(img.image.name)
                except Exception as e:
                    print(f'Backblaze error: {e}')
                img.delete()

            # Upload all new images
            for image in multiple_images:
                ListingImages.objects.create(listing=listing, image=image)
            
            #END MULTIMAGE PROCESSING    
                

            # return redirect('adminv2:listing')
            return JsonResponse({"success": True, "message": "Property updated successfully"})
        
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


def search_listing(request, search_query=None):
     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        listings = Listings.objects.all().order_by('-created_at')

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
        
        # TODO add is_listed to the filter
        # if is_listed:
        #     listings = listings.filter(is_listed__icontains=is_listed)
        

        return render(request, 'adminv2/listing/partials/listing-items.html', {
            'results': listings,
        })
     
    
@admin_only
def user_control_page(request):
    users = User.objects.all()
    return render(request, 'adminv2/users/users.html', {
        'users': users,
    })

@admin_only
@user_passes_test(lambda u: u.is_superuser)
def toggle_admin(request, user_id):
    """ This is used to promote a user into admin or demote a user into a customer """
    user = get_object_or_404(User, pk=user_id)
    try:
        if request.method == "POST":
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                
                if user.user_role == "admin":
                    if user.is_superuser:
                        return JsonResponse({
                            "success": False,
                            "user_role": user.user_role,
                            "message": f'This user cannot be demoted',
                        })
                    user.user_role = "customer"
                else:
                    user.user_role = "admin"
                
                user.save()
                
                return JsonResponse({
                    "success": True,
                    "user_role": user.user_role,
                    "message": f'{user.first_name} user role has been successfully changed',
                })
            
        return JsonResponse({
            "success": False,
            "message": "Invalid request",
        }, status=400)
    
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "User does not exist",
        }, status=400)

@admin_only
def user_info(request, user_id):
    """ To generate the information for a specific user. """
    user = get_object_or_404(User, pk=user_id)
    try:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'adminv2/users/partials/user-info.html', {
            'user': user,
        })

    except User.DoesNotExist:
        print("User does not exist")
        # return JsonResponse({
        #     "success": False,
        #     "message": "User does not exist",
        # }, status=400)


# messaging views
@admin_only
def message_page(request):
    return render(request, "adminv2/messaging/index.html")

@admin_only
def get_messages(request, message_id=None):

    messages = ContactMessage.objects.all().order_by('-sent_at')
    selected_sort = request.GET.get('selected_sort', '')
    sort_options = {
        'date_desc': '-sent_at',
        'date_asc': 'sent_at',
    }

    order_by_field = sort_options.get(selected_sort, '-sent_at') #default option '-created_at
    messages = messages.order_by(order_by_field)

    search_query = request.GET.get('search_query', '')
    if search_query:
        print("Hello")
        search_words = search_query.split()

        query = Q()
        for word in search_words:
            query |= Q(subject__icontains=word) | Q(body__icontains=word)
        messages = messages.filter(query)

    # to get a single message
    if message_id:
        message = get_object_or_404(ContactMessage, pk=message_id)
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request, 'adminv2/messaging/partials/message-info.html', {
                'message': message,
            })

        except ContactMessage.DoesNotExist:
            return JsonResponse({"success": False, "message": "User does not exist",}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "adminv2/messaging/partials/messages.html", {
            'messages': messages,
        })
    

@require_POST
@admin_only
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    try:
        message.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    