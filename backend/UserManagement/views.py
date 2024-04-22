from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse

class UserListView(APIView):
	def get(self, request):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return JsonResponse({"users": serializer.data})

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
	def get(self, request, id):
		try:
			user = User.objects.get(pk=id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def put(self, request, id):
		try:
			user = User.objects.get(pk=id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		try:
			user = User.objects.get(pk=id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
