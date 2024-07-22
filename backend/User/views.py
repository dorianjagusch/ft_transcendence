from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .mixins import UserMixin
from Friends.models import Friend
from .serializers import UserOutputSerializer, UserInputSerializer, UserFriendOutputSerializer

from shared_utilities.decorators import must_be_authenticated, \
	 								must_be_url_user, \
									valid_serializer_in_body

class UserListView(APIView, UserMixin):
	def get(self, request):
		if request.user.is_authenticated and request.GET.get("username_contains"):
			username_contains = request.GET.get("username_contains")
			users = User.objects.filter(username__contains=username_contains).exclude(id=request.user.id)
			## add error handling if either user doesn't exits or user is not authenticated
			serializer = UserFriendOutputSerializer(users, many=True, context={'request': request})
			return Response(serializer.data, status=status.HTTP_200_OK)

		users = User.objects.all()
		serializer = UserOutputSerializer(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):

		result = self.create_user(request)
		if not isinstance(result, User):
			return result

		outputSerializer = UserOutputSerializer(result)
		return Response(outputSerializer.data, status=status.HTTP_201_CREATED)

class UserDetailView(APIView, UserMixin):
	def get(self, request, user_id):
		result = self.get_user(user_id)
		if not isinstance(result, User):
			return result

		if self.is_request_from_specific_user(request, user_id):
			serializer = UserOutputSerializer(result)
			return Response(serializer.data)
		
		friendship = Friend.objects.get_friendship_status(request.user.id, result.id) # what is this line for?
		serializer = UserFriendOutputSerializer(result, context={'request': request})
		return Response(serializer.data)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def put(self, request, user_id):
		return self.update_user(request, user_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def delete(self, request, user_id):
		return self.delete_user(request, user_id)

class UserProfilePictureView(APIView, UserMixin):
	@method_decorator(csrf_exempt)
	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def post(self, request, user_id):
		return self.save_profile_picture(request, user_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def get(self, request, user_id):
		return self.get_profile_picture(user_id)

class UserLoginView(APIView, UserMixin):
	@method_decorator(csrf_exempt)
	def post(self, request):
		result = self.authenticate_user(request)
		if not isinstance(result, User):
			return result

		self.login_user(request, result)
		return Response(UserOutputSerializer(result).data, status=status.HTTP_202_ACCEPTED)

class UserLogoutView(APIView, UserMixin):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		return self.logout_user(request) # what happens if the user is not logged in?

# admin stuff, for debugging
class UserAdminDetailsView(APIView):
	def get(self, request):
		admins = User.objects.filter(is_superuser=True)
		serializer = UserOutputSerializer(admins, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		inputSerializer = UserInputSerializer(data=request.data)
		if inputSerializer.is_valid():
			username = inputSerializer.validated_data.get('username')
			password = inputSerializer.validated_data.get('password')
			user = User.objects.create_superuser(username=username, password=password)
			outputSerializer = UserOutputSerializer(user)
			return Response(outputSerializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(inputSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
