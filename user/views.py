from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from .tokens import email_verification_token
from .utils import send_verification_email, is_user_active

User = get_user_model()


def sign_up(request):

    """
    Handles user registration.
    """

    if request.user.is_authenticated:
        pass
    
    if request.method == 'POST':
        #handle ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                form = SignUpForm(data)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    send_verification_email(request, user)

                    return JsonResponse({'message': 'A verification link has been sent to your email. Please check your inbox and spam folder.'}, status=201)
                else:
                    return JsonResponse({'errors': form.errors}, status=400)
            
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # for tradtional submission
        else:
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('user:login')
    else:
        form = SignUpForm()

    return render(request, 'user/register.html', {'form':form})


def user_login(request):

    """
    Handles user authentication and login.
    """
    domain_name = request.get_host() 
    next_url = request.GET.get('next', 'core:home') #2nd arg is fallback if their is no next
    if next_url == '/user/logout':
        next_url = 'core:home' 
    full_url = f"{request.scheme}://{domain_name}{reverse(next_url)}"

    if request.user.is_authenticated:
        return redirect('core:home') #redirect if login

    if request.method == 'POST':
        
        #handle ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('password') 

            user = authenticate(request, email=email, password=password)
            
            
            if user: 
                print(user)             
                login(request, user)
                return JsonResponse({'message': 'Login successful', 'next_url': full_url}, status=200)

            user = User.objects.filter(email=email).first()
            if user:
                if not is_user_active(email):
                    send_verification_email(request, user)
                    return JsonResponse({'message': 'Verification email sent'}, status=403)
                
            return JsonResponse({'message': 'Invalid login details'}, status=401)

        else:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']  # Get email from the form
                password = form.cleaned_data['password']
                
                user = authenticate(request, email=email, password=password)  # Authenticate with email

                if user:
                    login(request, user) #login user
                    print('Working')
                    return redirect(next_url)
                else:
                    print('invalid credentials')
        
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form':form, 'next':next_url})



@login_required
def logout_view(request):
    logout(request)
    return redirect('user:login')


def activate_account(request, uidb64, token):
    """ verify user account using token """

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    #check token validity
    if user and email_verification_token.check_token(user, token):
        user.is_active = True #activate user
        user.save()
        messages.add_message(request, messages.SUCCESS, "Your account has been activated.")
        return redirect('user:login')
    
    return render(request, "user/activation_invalid.html", {"message": "Invalid activation link", "user_id": uid})


@require_POST
def resend_activation_token(request, uid):
    """ resending actiivation token """

    User = get_user_model()

    print(uid)

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found', 'type': 'error_message'}, status=400)

    if user.is_active:
        return JsonResponse({'message': 'User is already active', 'type': 'success_message'}, status=400)
    
    email_sent = send_verification_email(request, user)
    print("Email response", email_sent)
    if email_sent:
        return JsonResponse({'message': 'Email sent', 'type': 'success_message'}, status=201)
    else:
        return JsonResponse({'message': 'Error sending mail', 'type': 'error_message'}, status=500)


# forget password
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'emails/password_reset_email.txt'
    # subject_template_name = None
    success_message = "We have sent password reset instructions to your email."
    success_url = reverse_lazy('user:password_reset')

    def get_subject(self):
        return 'Reset Your Password'

    """     def get_email_context(self, user):
            
            return {
                "user": user,
                "email": user.email,  # Pass email explicitly if needed
                "domain": self.request.get_host(),
                "protocol": "https" if self.request.is_secure() else "http",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
    """
    def form_valid(self, form):

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            email = form.cleaned_data.get('email')
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    'message': 'This email is not registered with us.'
                }, status=400)

            response = super().form_valid(form)
            return JsonResponse({
                'message': 'We have sent password reset instructions to your email.'
            }, status=201)

        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, return an error message in JSON
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'message': 'There was an issue with your email. Please try again.'
            }, status=400)
        return super().form_invalid(form)