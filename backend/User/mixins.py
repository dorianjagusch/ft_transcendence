from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from .models import User

class UserAuthenticationMixin:
	def authenticate_user(self, request: Request) -> User | Response:
		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if not username or not password:
			return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
		
		user = authenticate(username, password)
		if user is not None:
			return user
		else:
			return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginMixin:
	def login_user(self, request: Request, user: User) -> None:
		login(request, user)
		request.session['is_authenticated'] = True