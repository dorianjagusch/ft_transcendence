from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from User.mixins import UserAuthenticationMixin
from User.models import User
from User.serializers import UserInputSerializer, \
								UserOutputSerializer
from .models import MatchToken
from .managers import MatchTokenManager
from .serializers import MatchTokenSerializer
from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											valid_serializer_in_body
import sys

# Create your views here.
class SingleMatchGuestTokenView(APIView, UserAuthenticationMixin):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		host_user = request.user
		ai_opponent = request.query_params.get('ai_opponent')
		if ai_opponent is not None and ai_opponent == 'true':
			token = MatchTokenManager.create_single_match_token(host_user, None)
			token_serializer = MatchTokenSerializer(token)
			return Response({
				'token': token_serializer.data,
				'guest_user': ''
			}, status=status.HTTP_201_CREATED)

		guest_authentication_result = self.authenticate_user(request)
		if not isinstance(guest_authentication_result, User):
			return guest_authentication_result

		token = MatchTokenManager.create_single_match_token(host_user, guest_authentication_result)
		token_serializer = MatchTokenSerializer(token)
		user_serializer = UserOutputSerializer(guest_authentication_result)
		return Response({
			'token': token_serializer.data,
			'guest_user': user_serializer.data
		}, status=status.HTTP_201_CREATED)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(MatchTokenSerializer))
	def put(self, request):
		try:
			token = MatchToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({"message": "Token has already expired"}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({"message": "Token is now expired"}, status=status.HTTP_200_OK)
		except MatchToken.DoesNotExist:
			return Response({"message": "Token was not found"}, status=status.HTTP_400_BAD_REQUEST)
