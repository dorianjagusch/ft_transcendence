from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .serializers import UserSerializer
from .decorators import user_is_object_owner

#  rm later
import sys

class UserListView(APIView):
	def get(self, request):
		users = CustomUser.objects.all()
		serializer = UserSerializer(users, many=True)
		return JsonResponse({"users": serializer.data})

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			# serializer.save()
			username = serializer.validated_data.get('username')
			password = serializer.validated_data.get('password')
			user = CustomUser.objects.create_user(username=username, password=password)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
	def get(self, request, user_id):
		try:
			user = CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	# @user_is_object_owner
	def put(self, request, user_id):
		try:
			user = CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@user_is_object_owner
	def delete(self, request, user_id):
		try:
			user = CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class UserLoginView(APIView):
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

