from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string

from .models import User
from .serializers import UserInputSerializer

class UserCreationMixin:
	def create_user(self, request: Request) -> User | Response:
		inputSerializer = UserInputSerializer(data=request.data)
		if not inputSerializer.is_valid():
			errors = inputSerializer.errors
			if 'username' in errors and 'exists' in errors['username'][0]:
				return Response(inputSerializer.errors, status=status.HTTP_409_CONFLICT)
			else:
				return Response(inputSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

		username = inputSerializer.validated_data.get('username')
		password = inputSerializer.validated_data.get('password')
		return User.objects.create_user(username=username, password=password)

class UserAuthenticationMixin:
	def authenticate_user(self, request: Request) -> User | Response:
		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if not username or not password:
			return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
		
		user = authenticate(request, username=username, password=password)
		if user is not None:
			return user
		else:
			return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginMixin:
	def login_user(self, request: Request, user: User) -> None:
		login(request, user)
		request.session['is_authenticated'] = True

class UserDeletionMixin:
	def delete_user(self, request: Request, user_id: int) -> Response:
		try:
			logout(request)
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		user.username = "deleted_user_" + str(user_id + 42)
		user.set_password(get_random_string(length=30))
		user.is_active = False
		user.is_staff = False
		user.is_superuser = False
		user.insertTS = None
		user.last_login = None
		user.is_online = False
		user.save()
		return Response(status=status.HTTP_204_NO_CONTENT)