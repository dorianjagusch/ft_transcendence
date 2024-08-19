from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .mixins import (
	GetAllUsersMixin, GetUsersWithUsernameContainsMixin, CreateUserMixin,
	GetUserMixin, DeleteUserMixin, UpdateUserMixin, AuthenticateUserMixin,
	LoginUserMixin, LogoutUserMixin, IsRequestFromSpecificUserMixin,
	SaveUserProfilePictureMixin, GetProfilePictureMixin
)
from .serializers import UserOutputSerializer, UserInputSerializer, UserFriendOutputSerializer
from shared_utilities.decorators import must_be_authenticated, must_be_url_user, valid_serializer_in_body


class UserListView(APIView, GetAllUsersMixin, GetUsersWithUsernameContainsMixin, CreateUserMixin):
	def get(self, request: Request) -> Response:
		if request.user.is_authenticated and request.GET.get("username_contains"):
			users = self.get_all_users_with_username_contains(request)
			serializer = UserFriendOutputSerializer(users, many=True, context={'request': request})
			return Response(serializer.data, status=status.HTTP_200_OK)

		users = self.get_all_users()
		serializer = UserOutputSerializer(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request: Request) -> Response:
		username = request.data.get('username')
		if User.objects.filter(username=username).exists():
			return Response({"message" : "User with username already exists"}, status=status.HTTP_409_CONFLICT)

		result = self.create_user(request)
		if not isinstance(result, User):
			return result

		output_serializer = UserOutputSerializer(result)
		return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class UserDetailView(APIView, GetUserMixin, IsRequestFromSpecificUserMixin, UpdateUserMixin, DeleteUserMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, user_id: int) -> Response:
		result = self.get_user(user_id)
		if not isinstance(result, User):
			return result

		if self.is_request_from_specific_user(request, user_id):
			serializer = UserOutputSerializer(result)
			return Response(serializer.data)

		serializer = UserFriendOutputSerializer(result, context={'request': request})
		return Response(serializer.data)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def put(self, request: Request, user_id: int) -> Response:
		return self.update_user(request, user_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def delete(self, request: Request, user_id: int) -> Response:
		return self.delete_user(request, user_id)

class UserProfilePictureView(APIView, SaveUserProfilePictureMixin, GetProfilePictureMixin):
	@method_decorator(csrf_exempt)
	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def post(self, request: Request, user_id: int) -> Response:
		return self.save_profile_picture(request, user_id)

	@method_decorator(must_be_authenticated)
	def get(self, request: Request, user_id: int) -> Response:
		return self.get_profile_picture(user_id)

class UserLoginView(APIView, AuthenticateUserMixin, LoginUserMixin):
	@method_decorator(csrf_exempt)
	def post(self, request: Request) -> Response:
		result = self.authenticate_user(request)
		if not isinstance(result, User):
			return result

		self.login_user(request, result)
		return Response(UserOutputSerializer(result).data, status=status.HTTP_202_ACCEPTED)

class UserLogoutView(APIView, LogoutUserMixin):
	@method_decorator(must_be_authenticated)
	def post(self, request: Request) -> Response:
		return self.logout_user(request)
