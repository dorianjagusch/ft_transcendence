from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.db import IntegrityError
import uuid

from .managers import UserManager, \
						AuthenticatedGuestUserTokenManager

# Create your models here.
class User(AbstractBaseUser):
	username = models.CharField(_('username'), max_length=30, null=False, blank=False, unique=True)
	password = models.CharField(_('password'), max_length=128, null=False, blank=False)
	
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('is_staff'), default=False)
	is_superuser = models.BooleanField(_('is_superuser'), default=False)
	insertTS = models.DateTimeField(_('insertTS'), auto_now_add=True, blank=True, null=True)
	last_login = models.DateTimeField(_('last_login'), blank=True, null=True)
	is_online = models.BooleanField(_('is_online'), default=False)
	
	# profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username


class AuthenticatedGuestUserToken(models.Model):
	host_user = models.ForeignKey(User, on_delete=models.CASCADE)
	guest_user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	objects = AuthenticatedGuestUserTokenManager()

	def save(self, *args, **kwargs):
		if self.host_user == self.guest_user:
			raise IntegrityError("host_user and guest_user cannot be the same.")
		super().save(*args, **kwargs)

	def is_expired(self):
		return self.created_at < datetime.now() - timedelta(minutes=5)

	def __str__(self):
		return str(self.token)