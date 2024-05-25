from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from User.models import User
from User.serializers import UserInputSerializer, \
								UserOutputSerializer

from .models import AuthenticatedGuestUserToken
from .serializers import AuthenticatedGuestUserTokenSerializer
from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											valid_serializer_in_body

# Create your views here.
class GuestUserAuthenticationView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(must_not_be_username)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):
		host_user = request.user
		username = request.data.get('username')
		password = request.data.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			token = AuthenticatedGuestUserToken.objects.get_or_create_token(host_user=host_user, guest_user=user)
			token_serializer = AuthenticatedGuestUserTokenSerializer(token)
			user_serializer = UserOutputSerializer(user)
			return Response({
                'token': token_serializer.data,
                'guest_user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
		
class DeactivateGuestUserTokenView(APIView):
	@method_decorator(valid_serializer_in_body(AuthenticatedGuestUserTokenSerializer))
	@method_decorator(must_be_authenticated)
	def post(self, request):
		try:
			token = AuthenticatedGuestUserToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({'message': 'Token has already expired'}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({'message': 'Token has expired'}, status=status.HTTP_200_OK)

		except AuthenticatedGuestUserToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)