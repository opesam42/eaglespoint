from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ContactMessageForm
from .models import ContactMessage

# Create your views here.

@require_POST
def api_create_contact_message(request):
    form = ContactMessageForm(request.POST)

    if form.is_valid():
        form = form.save()

        return JsonResponse({
            'success': True,
            'message': 'Your message has being successfully sent',
        }, status=201)
    
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)