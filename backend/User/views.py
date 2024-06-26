from functools import partial
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User
from Friends.models import Friend
from .serializers import UserOutputSerializer, UserInputSerializer, UserFriendOutputSerializer

from shared_utilities.decorators import must_be_authenticated, \
	 								must_be_url_user, \
									valid_serializer_in_body

class UserListView(APIView):
	def get(self, request):
		users = User.objects.all()
		serializer = UserOutputSerializer(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):

		inputSerializer = UserInputSerializer(data=request.data)
		if not inputSerializer.is_valid():
			errors = inputSerializer.errors
			if 'username' in errors and 'exists' in errors['username'][0]:
				return Response(inputSerializer.errors, status=status.HTTP_409_CONFLICT)
			else:
				return Response(inputSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

		username = inputSerializer.validated_data.get('username')
		password = inputSerializer.validated_data.get('password')
		user = User.objects.create_user(username=username, password=password)
		outputSerializer = UserOutputSerializer(user)
		return Response(outputSerializer.data, status=status.HTTP_201_CREATED)

class UserDetailView(APIView):
	def get(self, request, user_id):
		login_user_id = request.user.id
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		if user.id == login_user_id:
			serializer = UserOutputSerializer(user)
			return Response(serializer.data)
		friendship = Friend.objects.get_friendship_status(login_user_id, user.id)
		serializer = UserFriendOutputSerializer(user, friendship=friendship)
		return Response(serializer.data)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def put(self, request, user_id):
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		inputSerializer = UserInputSerializer(user, data=request.data, partial=True)
		if inputSerializer.is_valid():
			user = inputSerializer.save()
			outputSerializer = UserOutputSerializer(user)
			return Response(outputSerializer.data)
		else:
			return Response(inputSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def delete(self, request, user_id):
		try:
			logout(request)
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class UserLoginView(APIView):
	@method_decorator(csrf_exempt)
	def post(self, request):
		username_input = request.data.get('username')
		password_input = request.data.get('password')
		if not username_input or not password_input:
			return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

		user = authenticate(request, username=username_input, password=password_input)
		if user is not None:
			login(request, user)
			# set additional session data if necessary
			request.session['is_authenticated'] = True
			return Response({"message": "User login successful"}, status=status.HTTP_202_ACCEPTED)
		else:
			return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		logout(request)
		return Response({"message": "User logged out"}, status=status.HTTP_200_OK)

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
