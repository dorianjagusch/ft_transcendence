from django.db import models

from User.models import User
from .managers import FriendsManager

# Create your models here.
class Friend(models.Model):
	user_id = models.IntegerField()
	friend_id = models.IntegerField()
	insertTS = models.DateTimeField(auto_now_add=True)

	objects = FriendsManager()

	def __str__(self):
		return f"{self.user_id} - {self.friend_id} - {self.insertTS}"

	class Meta:
		# required because of RunTimeError that complains about lack of app_label
		app_label = 'Friends'
		constraints = [
			models.UniqueConstraint(fields=['user_id', 'friend_id'], name='unique_user_friend_pair')
		]

