from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Update user's is_online field when user logs in.
    """
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """
    Update user's is_online field when user logs out.
    """
    user.is_online = False
    user.save()
