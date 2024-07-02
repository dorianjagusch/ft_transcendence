from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
	username = models.CharField(_('username'), max_length=30, null=False, blank=False, unique=True)
	password = models.CharField(_('password'), max_length=128, null=False, blank=False)
	is_active = models.BooleanField(_('active'), default=True)
	is_superuser = models.BooleanField(_('is_superuser'), default=False)
	insertTS = models.DateTimeField(_('insertTS'), auto_now_add=True, blank=True, null=True)
	last_login = models.DateTimeField(_('last_login'), blank=True, null=True)
	is_online = models.BooleanField(_('is_online'), default=False)
	# profile_picture_path = models.CharField(_'profile_picture_path', max_length=200, blank=True, null=True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username
