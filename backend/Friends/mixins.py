from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet
from django.db import transaction

from .models import Friend
from .friendShipStatus import FriendShipStatus
from User.models import User


class GetUserFriendsMixin:
	"""
	Mixin for getting friends of a specific user.
	"""
	def get_user_friends(self, request: Request) -> QuerySet | Response:
		user_id = request.user.id
		friendship_status = request.query_params.get('friendship_status')
		if not friendship_status or friendship_status == FriendShipStatus.NONE.value:
			return Response({"message": "Expected to get parameter 'friendship_status'"}, status=status.HTTP_400_BAD_REQUEST)

		user_friends = Friend.objects.filter(user_id=user_id).values_list('friend_id', flat=True)
		friends_of_user = Friend.objects.filter(friend_id=user_id).values_list('user_id', flat=True)
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

class GetFriendshipStatusMixin:
	"""
	Mixin for getting friendship status of another user to own user.
	"""
	def get_friendship_status(self, user_id: int, friend_id: int) -> int:
		user_friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id)
		friend_user = Friend.objects.filter(user_id=friend_id, friend_id=user_id)
		if user_friend.exists() and friend_user.exists():
			return FriendShipStatus.FRIEND.value
		elif user_friend.exists():
			return FriendShipStatus.PENDINGSENT.value
		elif friend_user.exists():
			return FriendShipStatus.PENDINGRECEIVED.value
		else:
			return FriendShipStatus.NOTFRIEND.value

class CreateFriendshipMixin:
	"""
	Mixin for creating a user friendship.
	"""
	def create_friendship(self, request: Request) -> Friend | Response:
		user_id = request.user.id
		friend_id = request.data.get('friend_id')
		if user_id == friend_id:
			return Response({"message": "Can't add self as friend."}, status=status.HTTP_400_BAD_REQUEST)
		
		potential_friend = User.objects.filter(pk=friend_id).first()
		if not potential_friend:
			return Response({"message": "User to be added as friend does not exist."}, status=status.HTTP_400_BAD_REQUEST)
		if not potential_friend.is_active:
			return Response({"message": "Cannot add deleted user as friend."}, status=status.HTTP_400_BAD_REQUEST)
		
		return Friend.objects.create(user_id=user_id, friend_id=friend_id)

class DeleteFriendshipMixin:
	"""
	Mixin for deleting a user friendship.
	"""
	def delete_friendship(self, request: Request, friend_id: int) -> Response:
		user_id = request.user.id
		user = User.objects.filter(pk=friend_id, is_active=True).first()
		if not user:
			return Response({"message": "'Friend' user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
		
		user_friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id).first()
		friend_user = Friend.objects.filter(user_id=friend_id, friend_id=user_id).first()
		if not user_friend or not friend_user:
			return Response({"message": "No relation between user and 'friend'."}, status=status.HTTP_400_BAD_REQUEST)
		with transaction.atomic():
			if user_friend:
				user_friend.delete()
			if friend_user:
				friend_user.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteAllUserFriendshipsMixin:
	"""
	Mixin for deleting all friendships of a user.
	"""
	def delete_user_friendships(self, user: User) -> None:
		user_friends = Friend.objects.filter(user=user)
		friends_user = Friend.objects.filter(friend=user)

		try:
			with transaction.atomic():
				user_friends.delete()
				friends_user.delete()
		except Exception:
			pass
