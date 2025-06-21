from django.contrib.auth import logout
from django.http import JsonResponse

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_block or not request.user.is_active:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error',  'message': 'Account disabled'}, status=403)
                logout(request)

        return self.get_response(request)