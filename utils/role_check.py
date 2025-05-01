from django.shortcuts import render, redirect
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')
        if request.user.user_role != 'admin':
            return redirect('core:error_page')
        return view_func(request, *args, **kwargs)
    return wrapper

def is_admin(user):
    """Check if the user is an admin."""
    return user.user_role == 'admin'

def is_agent(user):
    """Check if the user is an agent."""
    return user.user_role == 'agent'

def is_customer(user):
    """Check if the user is a customer."""
    return user.user_role == 'customer'

def is_admin_or_agent(user):
    """Check if the user is either an admin or an agent."""
    return user.user_role in ['admin', 'agent']

def is_admin_or_customer(user):
    """Check if the user is either an admin or a customer."""
    return user.user_role in ['admin', 'customer']