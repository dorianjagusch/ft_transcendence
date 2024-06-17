from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import redirect

from .exceptions import MatchAndPlayersCreationException
from .managers import MatchSetupManager
from Tokens.models import MatchToken
from Tournament.models import Tournament, TournamentMatchup
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated

class MatchView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request):
		token_str = request.query_params.get('token')
		if not token_str:
			return Response({'error': 'Token parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			token = MatchToken.objects.get(token=token_str)
		except MatchToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

		if not token.is_active or token.is_expired():
			return Response({'error': 'Expired token'}, status=status.HTTP_403_FORBIDDEN)
		if token.tournament_matchup:
			if token.tournament_matchup.tournament.host_user != request.user:
				return Response({'error': 'You are not the host of the tournament'}, status=status.HTTP_403_FORBIDDEN)
		else:
			if token.user_left_side.id != request.user.id:
				return Response({'error': 'You are not the player_left_side (i.e. host user) in the token'}, status=status.HTTP_403_FORBIDDEN)

		try:
			match = MatchSetupManager.create_match_and_its_players(token)
			pong_match_url = f'ws://localhost:8080/pong/{match.id}?token={token.token}'

			return Response(pong_match_url, status=status.HTTP_200_OK)

		except MatchAndPlayersCreationException as e:
			return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LaunchTestMatchView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request):
		token = MatchToken.objects.create_single_match_token(request.user, request.user)
		  
		try:
			match_id = MatchSetupManager.create_match_and_its_players(token)
			pong_match_url = f'ws://localhost:8080/pong/{match_id}?token={token.token}'

			return Response(pong_match_url, status=status.HTTP_200_OK)
		
		except MatchAndPlayersCreationException as e:
		  return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)