from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
	username = models.CharField(max_length=30, null=False, blank=False, unique=True)
	password = models.CharField(max_length=128, null=False, blank=False)

	# profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

	def __str__(self):
		return self.username

class CustomUser(AbstractBaseUser):
	username = models.CharField(_('username'), max_length=30, null=False, blank=False, unique=True)
	password = models.CharField(_('password'), max_length=128, null=False, blank=False)

	# profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
 
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['username', 'password']

	def __str__(self):
		return self.username