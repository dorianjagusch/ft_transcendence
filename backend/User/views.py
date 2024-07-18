from functools import partial
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .validators import validate_image
from django.core.exceptions import ValidationError
import mimetypes
import imghdr
import base64
from django.utils.crypto import get_random_string

from .models import User, ProfilePicture
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

class UserProfilePictureView(APIView):
	@method_decorator(csrf_exempt)
	@method_decorator(must_be_authenticated)
	@method_decorator(must_be_url_user)
	def post(self, request, user_id):
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

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
			return Response(UserOutputSerializer(user).data, status=status.HTTP_202_ACCEPTED)
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
