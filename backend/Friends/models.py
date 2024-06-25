from django.db import models

from User.models import User
from .managers import FriendsManager

class Friend(models.Model):
	user = models.ForeignKey(User, related_name='users', null=False, blank=False, on_delete=models.CASCADE)
	friend = models.ForeignKey(User, related_name='friends', null=False, blank=False, on_delete=models.CASCADE)
	insertTS = models.DateTimeField(auto_now_add=True)

	objects = FriendsManager()

	def __str__(self):
		return f"{self.user.id} - {self.friend.id} - {self.insertTS}"

	class Meta:
		app_label = 'Friends'
		constraints = [
			models.UniqueConstraint(fields=['user', 'friend'], name='unique_user_friend_pair')
		]

