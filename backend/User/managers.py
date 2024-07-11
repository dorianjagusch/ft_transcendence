from django.db import models
from django.contrib.auth.models import BaseUserManager

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
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(username, password, **extra_fields)
