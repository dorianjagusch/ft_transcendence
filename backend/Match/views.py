from functools import partial
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import redirect

from User.models import User
from Tokens.models import AuthenticatedGuestUserToken
from Tokens.serializers import AuthenticatedGuestUserTokenSerializer
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated, \
											valid_serializer_in_body

from .models import Match

import sys

class LaunchSingleMatchView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(AuthenticatedGuestUserTokenSerializer))
	def post(self, request):
		try:
			token = AuthenticatedGuestUserToken.objects.get(token=request.data.get('token'))
		except AuthenticatedGuestUserToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

		if token.is_active == False or token.is_expired():
			return Response({'error': 'Expired token'}, status=status.HTTP_403_FORBIDDEN)
		if token.host_user.id != request.user.id:
			return Response({'error': 'You are not the host user in the token'}, status=status.HTTP_403_FORBIDDEN)
		
		match, host_player, guest_player = Match.objects.create_match_and_its_players(token.host_user.id, token.guest_user.id)

		if not all([match, host_player, guest_player]):
			return Response({'error': 'Something went wrong when creating the match and players'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		pong_match_url = f'http://localhost:80/pong/{match.id}?token={token.token}'
		return redirect(pong_match_url) # this is prob not correct as this is a single-page app...