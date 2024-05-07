from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)  # Update is_authenticated field when user logs in
def user_logged_in_handler(sender, request, user, **kwargs):
    user.is_online = True
    user.save()

@receiver(user_logged_out)  # Update is_authenticated field when user logs out
def user_logged_out_handler(sender, request, user, **kwargs):
    user.is_online = False
    user.save()