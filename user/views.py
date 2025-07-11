from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, AgentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import json
from django.db import OperationalError
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
from django.views.generic import TemplateView
from django.contrib.auth.forms import SetPasswordForm
from django.views.decorators.http import require_POST
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator

from .models import Agent
from .tokens import email_verification_token
from .utils import send_verification_email, is_user_active
from utils.storage import delete_cover_image_folder, get_signed_b2_url, BackBlazeAPI

from emails.views import send_account_verification_email
from messaging.forms import ContactMessageForm
from utils.role_check import require_ajax

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
                    send_account_verification_email(request, user, context={})
                    # send_verification_email(request, user)

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
    full_url = None
    next_url = request.GET.get('next', '') #2nd arg is fallback if their is no next
    print("Next_url", next_url)
    if next_url == '/user/logout':
        next_url = reverse('core:home')

    if next_url:
        full_url = f"{request.scheme}://{domain_name}{next_url}"
        request.session['full_url'] = full_url

    if request.user.is_authenticated:
        return redirect('core:home') #redirect if login

    if request.method == 'POST':
        
        #handle ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                email = data.get('username')
                password = data.get('password') 

                user = User.objects.filter(email=email).first()
                if user:
                    if not is_user_active(email):
                        send_verification_email(request, user)
                        return JsonResponse({'status':'error', 'error_type': 'user_not_verified', 'message': 'Verification email sent'}, status=403)
                    
                    if user.is_block:
                        return JsonResponse({'status': 'error', 'error_type': 'blocked_user', 'message': 'This account is blocked', 'redirect_url': reverse('user:unblock-account-page')})

                user = authenticate(request, email=email, password=password)                
                if user:         
                    login(request, user)
                    full_url = request.session.get('full_url')

                    if 'full_url' in request.session:
                        del request.session['full_url']

                    return JsonResponse({'status': 'success', 'message': 'Login successful', 'next_url': full_url}, status=200)
                    
                return JsonResponse({'status': 'error', 'error_type': 'invalid_credentials', 'message': 'Invalid login details'}, status=401)
            
            except OperationalError:
                return JsonResponse({'status': 'error', 'error_type': 'server_error', 'message': 'A server error has occured. Please try again later'}, status=500)
            except Exception as e:
                return JsonResponse({'status': 'error', 'error_type': 'unexpected_error', 'message': f'Unexpected error {str(e)}'}, status=500)

        else:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']  # Get email from the form
                password = form.cleaned_data['password']
                
                user = authenticate(request, email=email, password=password)  # Authenticate with email

                if user:
                    login(request, user) #login user
                    return redirect(next_url)
                else:
                    print('invalid credentials')
        
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form':form, 'next':next_url})


def logout_view(request):
    logout(request)
    return redirect('core:home')


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

@login_required
def user_settings(request):
    return render(request, 'user/settings.html')

@login_required
def update_profile(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
    
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')

        if 'profileImage' in request.FILES:
            old_profile_image = user.profileImage
            if old_profile_image:
                    # to delete the file
                    try:
                        backblaze = BackBlazeAPI()
                        backblaze.delete_files_with_prefix(old_profile_image.name)
                    except Exception as e:
                        print(f'Backblaze error: {e}')
                    
            user.profileImage = request.FILES['profileImage']

        user.save()
        # user.profileImage = data.get('profileImage')

        return JsonResponse({
            'success': True,
            'message': 'Profile successfully updated',
        })
    
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid Request',
        })


@login_required
@require_POST
def reset_password(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        if not user.check_password(old_password):
            return JsonResponse({
                'success': False,
                'message': 'Old password is incorrect',
            }, status=400)
        

        if old_password == new_password:
            return JsonResponse({
                'success': False,
                'message': "Your new password must be different from the current password."
            })

        if new_password != new_password2:
            return JsonResponse({
                'success': False,
                'message': 'The new passwords you entered do not match. Please try again.',
            }, status=400)
        
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': e.messages,
            }, status=400)

        user.set_password(new_password)
        user.save()
        # TODO: add email to be sent after password change
        update_session_auth_hash(request, user) #keep the user login after changing password

        return JsonResponse({'success': True, 'message': 'Password successfully updated.'})


def unblock_account_page(request):
    return render(request, 'user/unblock_account.html')

@require_POST
def unblock_request(request):
    """ 
        It handles sending the unblock request form.
        The function checks if the user exist and if he does, it check if the user's account is blocked. If not, return as invalid.
        But if it fulfil this condition, send the unblock request form using the ContactMessage Form 
    """

    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    post_data = request.POST.copy()
    post_data['subject'] = "Unblock Request" 
    email = post_data['sender_email']

    user = User.objects.filter(email=email).first()

    if not user:
        return JsonResponse({'status': 'error', 'error_type': 'user_not_found', 'message': 'No account found with this email address'}, status=404)
    
    if not user.is_block:
        return JsonResponse({'status': 'error', 'error_type': 'user_not_blocked', 'message': 'This account is not currently blocked'}, status=400)
    
    if user.phone_number:
        post_data['sender_phone'] = user.phone_number
    else:
        post_data['sender_phone'] = None

    post_data['sender_name'] = f"{user.first_name} {user.last_name}"
    

    form = ContactMessageForm(post_data)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Your unblock request has been submitted successfully!'}, status=201)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

def agent_form(request):
    form = AgentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Please login first")
            return redirect("user:agent-register-form")
        
        if request.POST['email'] != request.user.email:
                messages.error(request, "The email does not match your email. Check and try again")
                return redirect("user:agent-register-form")
        
        user = User.objects.filter(email=request.POST['email']).first()
        if not user:
            messages.error(request, "No user found with that email address.")
        
        if Agent.objects.filter(user=user):
           messages.error(request, "You are already registered as an agent. No further action is needed.") 

        user.user_role = 'agent'
        user.save()
        messages.success(request, "Your registration was successful! Please check your email for the next steps.")
        return redirect("user:agent-register-form")
    
    return render(request, 'user/agent_form.html')
                

def agent_form1(request):
    if request.method == "POST":
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:   
                post_data = request.POST.copy()
                post_data['user'] = request.user
                
                if not request.user.is_authenticated:
                    return JsonResponse({"status": "error", "message": "Authentication required"}, status=400)

                if post_data['email'] != request.user.email:
                    return JsonResponse({"status": "error", "message": "The email does not match your email. Check and try again"}, status=400)
                
                form = AgentForm(post_data)
                if form.is_valid:
                    form.save()
                    return JsonResponse({"status": "success", "message": "Agent created successfully"})
                
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)
            
            except OperationalError:
                return JsonResponse({'status': 'error', 'error_type': 'server_error', 'message': 'A server error has occured. Please try again later'}, status=500)
            except Exception as e:
                return JsonResponse({'status': 'error', 'error_type': 'unexpected_error', 'message': f'Unexpected error {str(e)}'}, status=500)

    return render(request, 'user/agent_form.html')

@require_ajax
@require_POST
def submit_agent_form(request):
    post_data = request.POST.copy()
    post_data['user'] = request.user
    
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=400)

    if post_data['email'] != request.user.email:
        return JsonResponse({"status": "error", "message": "The email does not match your email. Check and try again"}, status=400)
    
    form = AgentForm(post_data)
    if form.is_valid:
        form.save()
        return JsonResponse({"status": "success", "message": "Agent created successfully"})
    
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)



