from django.db import models

class User(models.Model):
	login = models.CharField(max_length=30)

	def __str__(self):
		return self.login
