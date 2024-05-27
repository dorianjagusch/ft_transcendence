from django.db import models
from .friendShipStatus import FriendShipStatus
from User.models import User
from django.db import transaction

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
		elif friendship_status == FriendShipStatus.NOTFRIEND.value:
			all_users = User.objects.exclude(id=user_id).values_list('id', flat=True)
			all_friends_and_pending = set(user_friends) | set(friends_of_user)
			friends_to_get = set(all_users) - all_friends_and_pending
		else:
			friends_to_get = set()
		friends = User.objects.filter(id__in=friends_to_get)
		return friends

	def get_friendship_status(self, user_id, friend_id):
		user_friend = self.filter(user_id=user_id, friend_id=friend_id)
		friend_user = self.filter(user_id=friend_id, friend_id=user_id)
		if user_friend.exists() and friend_user.exists():
			return FriendShipStatus.FRIEND.value
		elif user_friend.exists():
			return FriendShipStatus.PENDINGSENT.value
		elif friend_user.exists():
			return FriendShipStatus.PENDINGRECEIVED.value
		else:
			return FriendShipStatus.NOTFRIEND.value

	def get_friendship_by_user_and_friend_id(self, user_id, friend_id):
		return self.get(user_id=user_id, friend_id=friend_id)

	def get_friendship_by_id(self, friendship_id):
		return self.get(id=friendship_id)

	def create_friendship(self, user_id, friend_id):
		return self.create(user_id=user_id, friend_id=friend_id)

	def delete_friendship(self, user_id, friend_id):
		user_friend = self.filter(user_id=user_id, friend_id=friend_id)
		friend_user = self.filter(user_id=friend_id, friend_id=user_id)

		with transaction.atomic():
			if user_friend.exists():
				user_friend.delete()
			if friend_user.exists():
				friend_user.delete()


