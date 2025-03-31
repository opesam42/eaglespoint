from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from .tokens import email_verification_token
from .utils import send_verification_email


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

                    return JsonResponse({'message': 'Verification email sent'}, status=201)
                    # return redirect('user:login')
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

    next_url = request.GET.get('next', 'core:home') #2nd arg is fallback if their is no next
    if next_url == '/user/logout':
        next_url = 'core:home' #redirect to homepage

    if request.user.is_authenticated:
        return redirect('core:home') #redirect if login

    if request.method == 'POST':
        
        #handle ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('password')

            print(f"AJAX Login Attempt: email={email}, password={password}")
            user = authenticate(request, email=email, password=password)  # Authenticate with email
            
            if user:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid login details'}, status=401)

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

    User = get_user_model()

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    #check token validity
    if user and email_verification_token.check_token(user, token):
        user.is_active = True #activate user
        user.save()
        return redirect('user:login')
    
    else:
        return HttpResponse("Invalid link")
