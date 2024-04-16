from django.db import models

class User(models.Model):
	login = models.CharField(max_length=30, null=False, blank=False, unique=True)
	password = models.CharField(max_length=30, null=False, blank=False)
	# profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

	def __str__(self):
		return self.login
