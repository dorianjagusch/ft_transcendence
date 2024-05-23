from functools import partial
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from User.models import User
from User.serializers import AuthenticatedGuestUserToken
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated, \
											valid_serializer_in_body

from .models import Match

class LaunchSingleMatchView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(AuthenticatedGuestUserToken))
	def post(self, request):
		try:
			token = AuthenticatedGuestUserToken.objects.get(data=request.data.get('token'))
		except AuthenticatedGuestUserToken.DoesNotExist:
			return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
		if token.is_active == False or token.is_expired():
			return Response({'error': 'Expired token'}, status=status.HTTP_403_FORBIDDEN)
		if token.host_user != request.user.id:
			return Response({'error': 'You are not the host user in the token'}, status=status.HTTP_403_FORBIDDEN)
		
		match, host_player, guest_player = Match.objects.create_match(token.host_user, token.guest_user)