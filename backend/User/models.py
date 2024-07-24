from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager

class User(AbstractBaseUser):
	username = models.CharField('username', max_length=30, null=False, blank=False, unique=True)
	password = models.CharField('password', max_length=128, null=False, blank=False)
	is_active = models.BooleanField('active', default=True)
	is_superuser = models.BooleanField('is_superuser', default=False)
	insertTS = models.DateTimeField('insertTS', auto_now_add=True, blank=True, null=True)
	last_login = models.DateTimeField('last_login', blank=True, null=True)
	is_online = models.BooleanField('is_online', default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username

class ProfilePicture(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	picture = models.ImageField(upload_to='profile_pictures/')

	def __str__(self):
		return f"{self.user.username}'s Profile Picture"
