from django.contrib.auth.models import User

def get_user_list():
    # Example: Fetch all active users
    return User.objects.filter(is_active=True)