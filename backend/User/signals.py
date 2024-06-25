from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.request import Request
from django.dispatch import receiver
from typing import Type

from User.models import User

@receiver(user_logged_in)  # Update user's is_online field when user logs in
def user_logged_in_handler(sender: Type[User], request: Request, user: User, **kwargs: dict[str, any]) -> None:
    user.is_online = True
    user.save()

@receiver(user_logged_out)  # Update user's is_online field when user logs out
def user_logged_out_handler(sender: Type[User], request: Request, user: User, **kwargs: dict[str, any]) -> None:
    user.is_online = False
    user.save()