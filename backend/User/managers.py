from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db import transaction
from datetime import datetime

from .models import User, \
	                    AuthenticatedGuestUserToken

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        if not password:
            raise ValueError('The password field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
    

class AuthenticatedGuestUserTokenManager(models.Manager):
	def get_or_create_token(self, host_user, guest_user):
		with transaction.atomic():
			try:
				guest_token = AuthenticatedGuestUserToken.objects.filter(
					host_user=host_user,
					guest_user=guest_user
				).latest('created_at')

				if guest_token.is_expired():
					# If the latest token has expired, deactivate it and create a new one
					guest_token.is_active = False
					guest_token.save()
					guest_token = AuthenticatedGuestUserToken.objects.create(
						host_user=host_user,
						guest_user=guest_user
					)
				else:
					# If the latest token has not expired and is still active, update creation time, else create a new token
					if guest_token.is_active == True:
						guest_token.created_at = datetime.now() 
						guest_token.save()
					else:
						guest_token = AuthenticatedGuestUserToken.objects.create(
						host_user=host_user,
						guest_user=guest_user
						)
			except AuthenticatedGuestUserToken.DoesNotExist:
				# If no token exists, create a new one
				guest_token = AuthenticatedGuestUserToken.objects.create(
					host_user=host_user,
					guest_user=guest_user
				)

		return guest_token