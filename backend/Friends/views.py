from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from User.serializers import UserOutputSerializer
from .serializers import FriendInputSerializer, FriendOutputSerializer
from .mixins import GetUserFriendsMixin, CreateFriendshipMixin, DeleteFriendshipMixin
from shared_utilities.decorators import must_be_authenticated,valid_serializer_in_body

class FriendsListView(APIView, GetUserFriendsMixin, CreateFriendshipMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request) -> Response:
		result = self.get_user_friends(request)
		if isinstance(result, Response):
			response = result
			return response
		
		friends = result
		if not friends:
			friends = []
		serializer = UserOutputSerializer(friends, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(FriendInputSerializer, partial=True))
	def post(self, request: Request) -> Response:
		result = self.create_friendship(request)
		if isinstance(result, Response):
			response = result
			return response
		
		friend = result
		serializer = FriendOutputSerializer(friend)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendshipDetailView(APIView, DeleteFriendshipMixin):
	@method_decorator(must_be_authenticated)
	def delete(self, request: Request, friend_id: int) -> Response:
		return self.delete_friendship(request, friend_id)

