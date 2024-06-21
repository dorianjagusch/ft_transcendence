from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from User.models import User
from User.serializers import UserInputSerializer, \
								UserOutputSerializer

from .models import MatchToken
from .serializers import MatchTokenSerializer
from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											valid_serializer_in_body

# Create your views here.
class SingleMatchGuestTokenView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(must_not_be_username)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):
		host_user = request.user
		username = request.data.get('username')
		password = request.data.get('password')

		guest_user = authenticate(username=username, password=password)
		if guest_user is not None:
			token = MatchToken.objects.create_single_match_token(host_user, guest_user)
			token_serializer = MatchTokenSerializer(token)
			user_serializer = UserOutputSerializer(guest_user)
			return Response({
				'token': token_serializer.data,
				'guest_user': user_serializer.data
			}, status=status.HTTP_201_CREATED)
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(MatchTokenSerializer))
	def put(self, request):
		try:
			token = MatchToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({'message': 'Token has already expired'}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({'message': 'Token is now expired'}, status=status.HTTP_200_OK)
		except MatchToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
