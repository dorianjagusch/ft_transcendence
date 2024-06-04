from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone

from User.models import User
from .managers import AuthenticatedGuestUserTokenManager

class AbstractToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return str(self.token)


class AuthenticatedGuestUserToken(AbstractToken):
	host_user = models.ForeignKey(User, related_name='host_tokens', on_delete=models.CASCADE)
	guest_user = models.ForeignKey(User, related_name='guest_tokens', on_delete=models.CASCADE)
	

	objects = AuthenticatedGuestUserTokenManager()

	class Meta:
		constraints = [
			models.CheckConstraint(check=~models.Q(host_user=models.F('guest_user')), name='host_guest_not_same')
		]
