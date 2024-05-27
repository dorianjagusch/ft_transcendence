from django.db import models
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

class AuthenticatedGuestUserTokenManager(models.Manager):
	def get_or_create_token(self, host_user, guest_user):
		try:
			guest_token = self.get_queryset().filter(
				host_user=host_user,
				guest_user=guest_user
			).latest('created_at')

			if guest_token.is_expired():
				# If the latest token has expired, deactivate it and create a new one
				guest_token.is_active = False
				guest_token.save()
				guest_token = self.create(
					host_user=host_user,
					guest_user=guest_user
				)
			else:
				# If the latest token has not expired and is still active, update expires_at time, else create a new token
				if guest_token.is_active == True:
					guest_token.expires_at = timezone.now() + timedelta(minutes=5) 
					guest_token.save()
				else:
					guest_token = self.create(
					host_user=host_user,
					guest_user=guest_user
					)
		except models.ObjectDoesNotExist:
			# If no token exists, create a new one
			guest_token = self.create(
				host_user=host_user,
				guest_user=guest_user
			)

		return guest_token