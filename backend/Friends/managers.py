from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .friendShipStatus import FriendShipStatus
from User.models import User

class FriendsManager(models.Manager):
	def get_user_friends(self, user_id, friendship_status):
		user_friends = self.filter(user_id=user_id).values_list('friend_id', flat=True)
		friends_of_user = self.filter(friend_id=user_id).values_list('user_id', flat=True)
		friends_to_get = []
		if friendship_status == FriendShipStatus.PENDINGSENT.value:
			friends_to_get = set(user_friends) - set(friends_of_user)
		elif friendship_status == FriendShipStatus.PENDINGRECEIVED.value:
			friends_to_get = set(friends_of_user) - set(user_friends)
		elif friendship_status == FriendShipStatus.FRIEND.value:
			friends_to_get = set(friends_of_user) & set(user_friends)
		else:
			all_users = User.objects.exclude(id=user_id)
			friends_to_get = set(all_users.values_list('id', flat=True)) - (set(user_friends) | set(friends_of_user))
		friends = User.objects.filter(id__in=friends_to_get)
		return friends

	def get_friendship_by_user_and_friend_id(self, user_id, friend_id):
		return self.get(user_id=user_id, friend_id=friend_id)

	def get_friendship_by_id(self, friendship_id):
		return self.get(id=friendship_id)

	def create_friendship(self, user_id, friend_id):
		return self.create(user_id=user_id, friend_id=friend_id)

	def delete_friendship(self, user_id, friend_id):
		try:
			friendship = self.get(user_id=user_id, friend_id=friend_id)
			friendship.delete()
			return True
		except ObjectDoesNotExist:
			return False


