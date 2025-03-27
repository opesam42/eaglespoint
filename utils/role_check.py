
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