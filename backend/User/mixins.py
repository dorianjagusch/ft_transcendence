from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import base64

from .models import User, ProfilePicture
from .validators import validate_image, validate_password, validate_username
from .serializers import UserInputSerializer, UserOutputSerializer
from Friends.mixins import DeleteAllUserFriendshipsMixin

class GetAllUsersMixin:
	"""
	Mixin to get all Users.
	"""
	def get_all_users(self) -> QuerySet:
		return User.objects.filter(is_active=True)

class GetUsersWithUsernameContainsMixin:
	"""
	Mixin to get users whose username contains a specific substring.
	"""
	def get_all_users_with_username_contains(self, request: Request) -> QuerySet:
		username_contains = request.query_params.get("username_contains")
		if not username_contains:
			return User.objects.none()

		return User.objects.filter(username__icontains=username_contains, is_active=True).exclude(id=request.user.id)

class GetUserMixin:
	"""
	Mixin to get a user by ID.
	"""
	def get_user(self, user_id: int) -> User | Response:
		user = User.objects.filter(pk=user_id, is_active=True).first()
		if not isinstance(user, User):
				return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

		return user


class CreateUserMixin:
	"""
	Mixin to create a new user.
	"""
	def create_user(self, request: Request) -> User | Response:
		input_serializer = UserInputSerializer(data=request.data)
		if not input_serializer.is_valid():
			errors = input_serializer.errors
			if 'username' in errors and 'exists' in errors['username'][0]:
				return Response(input_serializer.errors, status=status.HTTP_409_CONFLICT)
			return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		username = input_serializer.validated_data.get('username')
		password = input_serializer.validated_data.get('password')
		try:
			validate_username(username)
			validate_password(password)
		except ValidationError as e:
			return Response({"message": e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
		return User.objects.create_user(username=username, password=password)


class UpdateUserMixin:
	"""
	Mixin to update a user by ID.
	"""
	def update_user(self, request: Request, user_id: int) -> Response:
		result = get_object_or_404(User, pk=user_id)
		if not isinstance(result, User):
				return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if not username and not password:
			return Response({"message": "Username or password are required to update information"}, status=status.HTTP_400_BAD_REQUEST)


		try:
			if password != None and password != '':
				validate_password(password)
				result.set_password(password)
			if username != None and username != '':
				validate_username(username)
				result.username = username
			result.save()
			outputSerializer = UserOutputSerializer(result)
			return Response(outputSerializer.data, status=status.HTTP_200_OK)
		except ValidationError as e:
			return Response({"message": e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
		except IntegrityError as e:
			return Response({"message": "User with username already exists"}, status=status.HTTP_409_CONFLICT)
		except Exception as e:
			return Response({"message": "Updating the user failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthenticateUserMixin:
	"""
	Mixin to authenticate a user.
	"""
	def authenticate_user(self, request: Request) -> User | Response:
		username = request.data.get('username')
		password = request.data.get('password')

		if not username or not password:
			return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

		user = authenticate(request, username=username, password=password)
		if user is not None:
			return user
		return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LoginUserMixin:
	"""
	Mixin to log a user in.
	"""
	def login_user(self, request: Request, user: User) -> None:
		login(request, user)
		request.session['is_authenticated'] = True


class LogoutUserMixin:
	"""
	Mixin to log a user out.
	"""
	def logout_user(self, request: Request) -> Response:
		logout(request)
		return Response({"message": "User logged out"}, status=status.HTTP_200_OK)

# used in DeleteUserMixin
def change_tournament_player_names_to_deleted(self, user: User) -> None:
		tournament_players = user.tournament_players.all()
		for player in tournament_players:
			player.display_name = "deleted_user"
			player.save()

class DeleteUserMixin(DeleteAllUserFriendshipsMixin):
	"""
	Mixin to delete a user by ID.
	"""
	def delete_user(self, request: Request, user_id: int) -> Response:
		try:
			logout(request)
		except Exception:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		result = get_object_or_404(User, pk=user_id)
		if not isinstance(result, User):
				response = result
				return response

		user = result
		user.username = f"deleted_user_{user_id + 42}"
		user.set_password(get_random_string(length=30))
		user.is_active = False
		user.is_staff = False
		user.is_superuser = False
		user.insert_ts = None
		user.last_login = None
		user.is_online = False
		user.save()
		profile_picture = ProfilePicture.objects.filter(user=user).first()
		if profile_picture:
			profile_picture.delete_profile_picture()
			profile_picture.delete()

		change_tournament_player_names_to_deleted(user)
		self.delete_user_friendships(user)

		return Response(status=status.HTTP_204_NO_CONTENT)


class SaveUserProfilePictureMixin(GetUserMixin):
	"""
	Mixin to save a user's profile picture.
	"""
	def save_profile_picture(self, request: Request, user_id: int) -> Response:
		result = self.get_user(user_id)
		if not isinstance(result, User):
				return result

		if 'file' not in request.FILES:
			return Response({"message": "File not provided in the request"}, status=status.HTTP_400_BAD_REQUEST)

		file = request.FILES['file']

		try:
			validate_image(file)
		except ValidationError as e:
			return Response({"message": e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)

		try:
			profile_picture = ProfilePicture.objects.get(user=result)
			profile_picture.update_profile_picture(file)
		except ProfilePicture.DoesNotExist:
			profile_picture = ProfilePicture(user=result, picture=file)
			profile_picture.save()
		return Response(status=status.HTTP_200_OK)


class GetProfilePictureMixin(GetUserMixin):
	"""
	Mixin to get a user's profile picture.
	"""
	def get_profile_picture(self, user_id: int) -> Response:
		try:
			result = self.get_user(user_id)
			if not isinstance(result, User):
				return result

			profile_picture = ProfilePicture.objects.filter(user=result).first()
			if not profile_picture:
				return Response({'image': ''}, status=status.HTTP_200_OK)

			image_path = profile_picture.picture.path
			with open(image_path, "rb") as image_file:
				image_data = image_file.read()
				encoded_image = base64.b64encode(image_data).decode('utf-8')
				return Response({'image': encoded_image}, status=status.HTTP_200_OK)
		except FileNotFoundError:
			return Response(status=status.HTTP_404_NOT_FOUND)


class IsRequestFromSpecificUserMixin:
	"""
	Mixin to check if the request is from a specific user.
	"""
	def is_request_from_specific_user(self, request: Request, user_id: int) -> bool:
		return request.user.id == user_id
