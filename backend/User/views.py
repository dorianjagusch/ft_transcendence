from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserOutputSerializer, UserInputSerializer

from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated, \
	 								must_be_url_user, \
									valid_serializer_in_body

# rm later
import sys

class UserListView(APIView):
	def get(self, request):
		users = User.objects.all()
		serializer = UserOutputSerializer(users, many=True)
		return JsonResponse({"users": serializer.data})

	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):

		print("in UserListView POST", file=sys.stderr)

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
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = UserOutputSerializer(user)
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
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
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

# admin stuff, for debugging
class UserAdminDetailsView(APIView):
	def get(self, request):
		admins = User.objects.filter(is_superuser=True)
		serializer = UserOutputSerializer(admins, many=True)
		return JsonResponse({"admins": serializer.data})

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
