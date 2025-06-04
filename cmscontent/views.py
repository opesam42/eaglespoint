from django.shortcuts import render, get_object_or_404
from .models import Testimonial, FAQ, TeamMember, Partners
from utils.role_check import is_admin, admin_only
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from .forms import TestimonialForm, TeamMemberForm, FAQForm, PartnerForm
# Create your views here.


@admin_only
@require_POST
def create_testimonial(request):
    form = TestimonialForm(request.POST)

    if form.is_valid():
        form = form.save()

        return JsonResponse({
            'success': True,
            'message': 'Testimonial was successfully added.',
        }, status=201)
    
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)


@admin_only
@require_POST
def update_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)

    form = TestimonialForm(request.POST, instance=testimonial)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Testimonial updated successfully.'})

    else:
        # Return form errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
@admin_only
def delete_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)

    try:
        testimonial.delete()
        return JsonResponse({"success": True, "message": "Testimonial successfully deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@admin_only
@require_POST
def create_team_member(request):
    form = TeamMemberForm(request.POST, request.FILES)

    if form.is_valid():
        form = form.save()

        return JsonResponse({
            'success': True,
            'message': 'Team member was successfully added.',
        }, status=201)
    
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)
    


@admin_only
@require_POST
def update_team_member(request, id):
    team_member = get_object_or_404(TeamMember, id=id)

    form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Team member updated successfully.'})

    else:
        # Return form errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_only
@require_POST
def save_order_team_member(request):
    print('hello')
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        print("Items", items)
        for index, item in enumerate(items):
            TeamMember.objects.filter(pk=item['id']).update(order=index)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)


@require_POST
@admin_only
def delete_team_member(request, id):
    team_member = get_object_or_404(TeamMember, id=id)

    try:
        team_member.delete()
        return JsonResponse({"success": True, "message": "Team member successfully deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    

@admin_only
@require_POST
def add_faq(request):
    form = FAQForm(request.POST)

    if form.is_valid():
        form = form.save()

        return JsonResponse({
            'success': True,
            'message': 'FAQ was successfully added.',
        }, status=201)
    
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)
    

@admin_only
@require_POST
def update_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)

    form = FAQForm(request.POST, instance=faq)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'FAQ updated successfully.'})

    else:
        # Return form errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@admin_only
@require_POST
def save_order_faqs(request):
    print('hello')
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        print("Items", items)
        for index, item in enumerate(items):
            FAQ.objects.filter(pk=item['id']).update(order=index)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

@require_POST
@admin_only
def delete_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)

    try:
        faq.delete()
        return JsonResponse({"success": True, "message": "FAQ successfully deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    


@admin_only
@require_POST
def add_partner(request):
    form = PartnerForm(request.POST, request.FILES)

    if form.is_valid():
        form = form.save()

        return JsonResponse({
            'success': True,
            'message': 'Saved successfully.',
        }, status=201)
    
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)
    

@admin_only
@require_POST
def update_partner(request, id):
    partner = get_object_or_404(FAQ, id=id)

    form = PartnerForm(request.POST, request.FILES, instance=partner)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Updated successfully.'})

    else:
        # Return form errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@admin_only
@require_POST
def save_order_partner(request):
    print('hello')
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        print("Items", items)
        for index, item in enumerate(items):
            Partners.objects.filter(pk=item['id']).update(order=index)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

@require_POST
@admin_only
def delete_partner(request, id):
    partner = get_object_or_404(Partners, id=id)

    try:
        partner.delete()
        return JsonResponse({"success": True, "message": "Successfully deleted"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})