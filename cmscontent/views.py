from django.shortcuts import render, get_object_or_404
from .models import Testimonial, FAQ
from utils.role_check import is_admin, admin_only
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import TestimonialForm
# Create your views here.



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
    print("Data", request.POST)
    
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