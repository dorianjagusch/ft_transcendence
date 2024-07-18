from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from User.serializers import UserOutputSerializer
from .models import Friend
from User.models import User, ProfilePicture
from .serializers import FriendInputSerializer, FriendOutputSerializer
from .friendShipStatus import FriendShipStatus
from shared_utilities.decorators import must_be_authenticated, \
									must_be_body_user_id, \
									valid_serializer_in_body
import base64

class FriendsListView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request):
		friendship_status = request.query_params.get('friendship_status')
		if not friendship_status or friendship_status == FriendShipStatus.NONE.value:
			return Response({"message": "Expected to get parameter 'friendship_status'"}, status=status.HTTP_400_BAD_REQUEST)
		user_id = request.user.id
		friends = Friend.objects.get_user_friends(user_id, friendship_status)

		if not friends:
			friends = []
		serializer = UserOutputSerializer(friends, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(FriendInputSerializer, partial=True))
	def post(self, request):
		user_id = request.user.id
		friend_id = request.data.get('friend_id')
		if user_id == friend_id:
			return Response({"message": "Can't add friendship for self."}, status=status.HTTP_400_BAD_REQUEST)
		try:
			friend = Friend.objects.create_friendship(user_id, friend_id)
		except Exception as e:
			# TODO: ADD ERROR for conflict 409 if friendship in the desired direction already exists
			return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		serializer = FriendOutputSerializer(friend)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendshipDetailView(APIView):
	@method_decorator(must_be_authenticated)
	def delete(self, request, friend_id):
		user_id = request.user.id
		try:
			Friend.objects.delete_friendship(user_id, friend_id)
		except Exception as e:
			# TODO: 404 if friendship does not exist
			return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_204_NO_CONTENT)

class FriendProfilePictureView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request, user_id):
		try:
			user = User.objects.get(pk=user_id)
			profile_picture = ProfilePicture.objects.filter(user=user).first()
			if not profile_picture:
				return Response({'image': ''}, status=status.HTTP_200_OK)

			image_path = profile_picture.picture.path
			with open(image_path, "rb") as image_file:
				image_data = image_file.read()
				encoded_image = base64.b64encode(image_data).decode('utf-8')
				return Response({'image': encoded_image}, status=status.HTTP_200_OK)
		except ProfilePicture.DoesNotExist:
			return Response({'image': ''}, status=status.HTTP_200_OK)
		except FileNotFoundError:
			return Response(status=status.HTTP_404_NOT_FOUND)
