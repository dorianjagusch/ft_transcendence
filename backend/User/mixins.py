from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import base64

from .models import User, ProfilePicture
from .validators import validate_image
from .serializers import UserInputSerializer, UserOutputSerializer

class GetAllUsersMixin:
    """
    Mixin to get all Users.
    """
    def get_all_users(self) -> QuerySet:
        return User.objects.all()
    
class GetUsersWithUsernameContainsMixin:
    """
    Mixin to get users whose username contains a specific substring.
    """
    def get_all_users_with_username_contains(self, request: Request) -> QuerySet:
        username_contains = request.query_params.get("username_contains")
        if not username_contains:
            return User.objects.none()
        
        return User.objects.filter(username__icontains=username_contains).exclude(id=request.user.id)

class GetUserMixin:
    """
    Mixin to get a user by ID.
    """
    def get_user(self, user_id: int) -> User | Response:
        return get_object_or_404(User, pk=user_id)


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
        return User.objects.create_user(username=username, password=password)


class UpdateUserMixin:
    """
    Mixin to update a user by ID.
    """
    def update_user(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        if not isinstance(user, User):
            return user

        input_serializer = UserInputSerializer(user, data=request.data, partial=True)
        if input_serializer.is_valid():
            input_serializer.save()
            output_serializer = UserOutputSerializer(user)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class DeleteUserMixin:
	"""
	Mixin to delete a user by ID.
	"""
	def delete_user(self, request: Request, user_id: int) -> Response:
		try:
			logout(request)
		except Exception:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		user = get_object_or_404(User, pk=user_id)
		if not isinstance(user, User):
				return user

		user.username = f"deleted_user_{user_id + 42}"
		user.set_password(get_random_string(length=30))
		user.is_active = False
		user.is_staff = False
		user.is_superuser = False
		user.insertTS = None
		user.last_login = None
		user.is_online = False
		user.save()
		return Response(status=status.HTTP_204_NO_CONTENT)


class SaveUserProfilePictureMixin:
    """
    Mixin to save a user's profile picture.
    """
    def save_profile_picture(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        if not isinstance(user, User):
             return user

        if 'file' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']

        try:
            validate_image(file)
        except ValidationError as e:
            return Response({"message": e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile_picture = ProfilePicture.objects.get(user=user)
            profile_picture.picture = file
        except ProfilePicture.DoesNotExist:
            profile_picture = ProfilePicture(user=user, picture=file)
        
        profile_picture.save()
        return Response(status=status.HTTP_200_OK)


class GetProfilePictureMixin:
    """
    Mixin to get a user's profile picture.
    """
    def get_profile_picture(self, user_id: int) -> Response:
        try:
            user = get_object_or_404(User, pk=user_id)
            if not isinstance(user, User):
                 return user
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


class IsRequestFromSpecificUserMixin:
    """
    Mixin to check if the request is from a specific user.
    """
    def is_request_from_specific_user(self, request: Request, user_id: int) -> bool:
        return request.user.id == user_id
