from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def sign_up(request):

    """
    Handles user registration.
    """

    if request.user.is_authenticated:
        pass
    
    if request.method == 'POST':
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