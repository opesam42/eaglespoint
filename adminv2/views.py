from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
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
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from listing.models import Listings
from utils.storage import delete_cover_image_folder, append_image_prefix, BackBlazeAPI
from messaging.models import ContactMessage
from cmscontent.models import Testimonial, FAQ, TESTIMONIAL_CATEGORIES, TeamMember, Partners
from blog.models import BlogArticle
from blog.forms import BlogArticleForm

User = get_user_model()


# Create your views here.
@admin_only
def dashboard(request):
    users_count = User.objects.count()
    listings_count = Listings.objects.count()
    articles_count = BlogArticle.objects.count()
    breadcrumbs = [
        {'title': 'Home', 'url': None},
    ]

    context = {
        'users_count': users_count,
        'listings_count': listings_count,
        'articles_count': articles_count,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'adminv2/dashboard.html', context)

@admin_only
def listing(request):
    listings = Listings.objects.all()
    nigeria_states = Listings.objects.values_list('state', flat=True).order_by('state').distinct()

    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Listing', 'url': None}
    ]

    return render(request, 'adminv2/listing/listing.html', {
        'results': listings,
        'nigeria_states': nigeria_states,
        'breadcrumbs': breadcrumbs,
    })


@require_POST
@admin_only
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)

    try:
        listing.delete()
        listing_media_dir = f'listing-images/listing_{listing_id}/'

        try:
            backblaze = BackBlazeAPI()
            backblaze.delete_files_with_prefix(listing_media_dir)
        except Exception as e:
            print(f'Backblaze error: {e}')

        return JsonResponse({"success": True, "message": "Listing successfully deleted"})
        # return redirect('adminv2:listing')
    except Exception as e:
        return JsonResponse({'success': False, 'error':str(e)}, status=500)
    
    # return redirect('adminv2:listing')


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
        breadcrumbs = [
            {'title': 'Home', 'url': reverse('adminv2:dashboard')},
            {'title': 'Listings', 'url': reverse('adminv2:listing')},
            {'title': 'Add Listing', 'url': None}
        ]

    context = {
        'form': form,
        'listing_types': LISTING_TYPE,
        'nigeria_states': STATE_CHOICES,
        'features': Feature.objects.all(),
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'adminv2/listing/add.html', context)



@admin_only
def edit_listing(request, property_id):
    
    listingEdit = get_object_or_404(Listings, id=property_id)
    
    # listingImages = [f"/media/{image}" for image in ListingImages.objects.filter(listing_id=property_id).values_list('image', flat=True)]
    # listingImageArray = mark_safe(json.dumps(listingImages).replace('"', "'"))

    property_images = ListingImages.objects.filter(listing_id=property_id).values_list('image', flat=True)
    signed_image_urls = [append_image_prefix(img) for img in property_images]
    listingImageArray = mark_safe(json.dumps(signed_image_urls))

    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Listings', 'url': reverse('adminv2:listing')},
        {'title': 'Update Listing', 'url': None}
    ]
    
    
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
        'listing_images': listingImageArray,
        'breadcrumbs': breadcrumbs,
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
    return render(request, 'adminv2/users/users.html')

@admin_only
def get_users(request, message_id=None):

    users = User.objects.all()

    selected_sort = request.GET.get('selected_sort', '')
    page_number = request.GET.get('page', 1)

    sort_options = {
        'date_desc': '-date_joined',
        'date_asc': 'date_joined',
    }

    order_by_field = sort_options.get(selected_sort, '-date_joined') 
    users = users.order_by(order_by_field)

    search_query = request.GET.get('search_query', '')
    if search_query:
        search_words = search_query.split()

        query = Q()
        for word in search_words:
            query |= Q(first_name__icontains=word) | Q(last_name__icontains=word) | Q(email__icontains=word) | Q(phone_number__icontains=word)
        users = users.filter(query)

    user_role = request.GET.get('user_role', '')
    active_status = request.GET.get('active_status', '')

    if user_role:
        users = users.filter(user_role=user_role)
    
    if active_status == '1':
        users = users.filter(is_active=True)
    elif active_status == '0':
        users = users.filter(is_active=False)
    
    paginator = Paginator(users, 10)
    users = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "adminv2/users/partials/users-table.html", {
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
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Inbox', 'url':None},
    ]
        
    return render(request, "adminv2/messaging/index.html", {'breadcrumbs': breadcrumbs})

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
            query |= Q(subject__icontains=word) | Q(body__icontains=word) | Q(sender_name__icontains=word)
        messages = messages.filter(query)

    page_number = request.GET.get('page', 1)

    paginator = Paginator(messages, 10)
    messages = paginator.get_page(page_number)


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
    
@admin_only
def cms_admin_page(request):
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'CMS', 'url':None},
    ]
    return render(request, 'adminv2/cms/index.html', { 'breadcrumbs': breadcrumbs })

@admin_only
def testimonial_partial(request):
    testimonials = Testimonial.objects.all().order_by('created_at')
    return render(request, 'adminv2/cms/partials/testimonial/testimonials.html', {'testimonials': testimonials, 'categories': TESTIMONIAL_CATEGORIES})

@admin_only
def faqs_partial(request):
    faqs = FAQ.objects.all().order_by('order')
    faqs_json = [
        {
            'id': faq.id,
            'question': faq.question,
            'answer': faq.answer,
            'order': faq.order,
            'is_active': faq.is_active,
        }
        for faq in faqs
    ]

    print("Pre", faqs_json)
    faqs_json = json.dumps(faqs_json)
    print("Post", faqs_json)

    context = {
        'faqs': faqs,
        'faqs_json': faqs_json,
    }
    return render(request, 'adminv2/cms/partials/faq/faqs.html', context)

@admin_only
def team_partial(request):
    team_members = TeamMember.objects.all().order_by('order')
    team_members_json = [
        {
            'id': member.id,
            'name': member.name,
            'position': member.position,
            'photo': member.photo.url if member.photo else '',  # Safely get the full URL
        }
        for member in team_members
    ]


    context = {
        'team_members': team_members,
        'team_members_json': team_members_json,
    }
    return render(request, 'adminv2/cms/partials/team/team.html', context)

@admin_only
def render_testimonial_form(request):
    return render(request, 'adminv2/cms/partials/testimonial/new-testimonial-form.html', {'categories': TESTIMONIAL_CATEGORIES})

def render_update_testimonial_form(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    return render(request, 'adminv2/cms/partials/testimonial/update-testimonial-form.html', {'testimonial': testimonial, 'categories': TESTIMONIAL_CATEGORIES})


@admin_only
def blog_index_page(request):
    categories = BlogArticle.ARTICLE_CATEGORY
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Blog Articles', 'url':None},
    ]

    return render(request, 'adminv2/blog/index.html', {'categories': categories, 'breadcrumbs': breadcrumbs})


@require_POST
@admin_only
def create_blog(request):
    form = BlogArticleForm(request.POST, request.FILES)

    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        try:
            blog.save()
        except Exception as e:
            print("Error saving blog:", e)
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

        return JsonResponse({
            'success': True, 'message': 'New blog article has been added.', 'blog_slug': blog.slug}, status=201)
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    

@admin_only
def display_blog_form(request):
    form = BlogArticleForm(request.POST, request.FILES)
    categories = BlogArticle.ARTICLE_CATEGORY
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Blog Articles', 'url': reverse('adminv2:display-blog-form')},
        {'title': 'Create Blog Article', 'url':None},
    ]

    context = {
        'form': form,
        'categories': categories,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'adminv2/blog/create-blog.html', context)


@require_POST
@admin_only
def blog_update(request, id):
    blogArticle = get_object_or_404(BlogArticle, id=id)
    form = BlogArticleForm(request.POST, request.FILES, instance=blogArticle)
    
    if form.is_valid():
        blog = form.save()
        return JsonResponse({'success': True, 'message': 'Blog article updated successfully.', 'blog_slug': blog.slug})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_only
def display_update_blog_form(request, id):
    blogArticle = get_object_or_404(BlogArticle, id=id)
    form = BlogArticleForm(request.POST, request.FILES)
    categories = BlogArticle.ARTICLE_CATEGORY
    breadcrumbs = [
        {'title': 'Home', 'url': reverse('adminv2:dashboard')},
        {'title': 'Blog Articles', 'url': reverse('adminv2:display-blog-form')},
        {'title': 'Update Blog Article', 'url':None},
    ]

    context = {
        'form': form,
        'categories': categories,
        'article': blogArticle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'adminv2/blog/update-blog.html', context)


@require_POST
@admin_only
def delete_article(request, id):
    article = get_object_or_404(BlogArticle, id=id)

    try:
        article.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    

@require_POST
@admin_only
def change_publish_status(request, id):
    article = get_object_or_404(BlogArticle, id=id)

    try:
        if article.published == True:
            article.published = False
        else:
            article.published = True

        article.save()
        return JsonResponse({"success": True, "message": "Article publishing status has being changed"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



@admin_only
def render_add_member_form(request):
    return render(request, 'adminv2/cms/partials/team/add-member.html')

@admin_only
def render_edit_member_form(request, id):
    member = get_object_or_404(TeamMember, id=id)
    return render(request, 'adminv2/cms/partials/team/edit-member.html', {'member': member})

@admin_only
def render_add_faq_form(request):
    return render(request, 'adminv2/cms/partials/faq/add-faq.html')

@admin_only
def render_update_faq_form(request, id):
    faq = get_object_or_404(FAQ, id=id)
    return render(request, 'adminv2/cms/partials/faq/update-faq.html', {'faq': faq})

@admin_only
def partners_partial(request):
    partners = Partners.objects.all(). order_by('-order')
    partners_json = [
        {
            'id': partner.id,
            'name': partner.name,
            'logo': partner.logo.url if partner.logo else '',
        }
        for partner in partners
    ]

    context = {
        'partners': partners,
        'partners_json': partners_json
    }
    return render(request, 'adminv2/cms/partials/partners/partners.html', context)


@admin_only
def render_add_partner_form(request):
    return render(request, 'adminv2/cms/partials/partners/add-partner.html')

@admin_only
def render_update_partner_form(request, id):
    partner = get_object_or_404(Partners, id=id)
    return render(request, 'adminv2/cms/partials/partners/update-partner.html', {'partner': partner})

