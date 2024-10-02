from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Match
from .serializers import MatchSerializer
from Player.models import Player
from Tokens.models import MatchToken
from User.models import User

# used in GetMatchUrlMixin
def create_match_and_its_players(match_token: MatchToken) -> Match | None:
		try:
			with transaction.atomic():
				match = Match.objects.create()

				Player.objects.create(
					user_id=match_token.user_left_side.id,
					match=match,
					score=0,
					match_winner=False
				)

				if match_token.user_right_side is not None:
					Player.objects.create(
						user_id=match_token.user_right_side.id,
						match=match,
						score=0,
						match_winner=False
					)

		except Exception as e:
			return None

		return match

class GetMatchUrlMixin:
	"""
	Mixin for getting the url for a match game.
	Sets up the Match and its players with the match token that is passed as a query parameter.
	"""
	def get_match_url(self, request: Request) -> Response:
		token_str = request.query_params.get('token')
		if not token_str or token_str == 'null':
			return Response({"message": "Token parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			token = MatchToken.objects.get(token=token_str)
		except Exception:
			return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

		if token.already_used_to_get_url == True:
			return Response({"message": "Token already used to get match url."}, status=status.HTTP_403_FORBIDDEN)
		token.already_used_to_get_url = True
		token.save()

		if not token.is_active or token.is_expired():
			return Response({"message": "Expired token."}, status=status.HTTP_403_FORBIDDEN)
		if token.user_left_side.id != request.user.id:
			return Response({"message": "You are not the host user in the token."}, status=status.HTTP_401_UNAUTHORIZED)

		match = create_match_and_its_players(token)

		if not match:
			return Response({"message": "Something went wrong when creating the match and players."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		pong_match_url = f'wss://localhost:8443/pong/{match.id}?token={token.token}'
		return Response(pong_match_url, status=status.HTTP_200_OK)

class GetUserMatchHistoryMixin:
	"""
	Mixin for getting a user's match history.
	"""
	def get_user_match_history(self, request: Request) -> Response:
		user_id = request.query_params.get('user_id')
		user = get_object_or_404(User, pk = user_id)
		if not isinstance(user, User):
			return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
		matches = Match.objects.filter(players__user=user).distinct()
		serializer = MatchSerializer(matches, many = True)
		for match in matches:
			if match.start_ts and timezone.is_naive(match.start_ts):
				match.start_ts = timezone.make_aware(match.start_ts)
			if match.end_ts and timezone.is_naive(match.end_ts):
				match.end_ts = timezone.make_aware(match.end_ts)

		return Response(serializer.data, status=status.HTTP_200_OK)
	
class GetMatchDetailsMixin:
	"""
	Mixin for getting info of a specific match
	"""
	def get_match_details(self, match_id: int) -> Response:
		match = get_object_or_404(Match, pk=match_id)
		if not isinstance(match, Match):
			return Response({"message": "Match not found"}, status=status.HTTP_404_NOT_FOUND)

		players = Player.objects.filter(match_id=match_id)
		if not players:
			return Response({"message": "Match players not found"}, status=status.HTTP_404_NOT_FOUND)

		if players.count() == 1:
			player = players.first()
			if player.match_winner:
				winner = player.user.username
				loser = 'AI'
			else:
				winner = 'AI'
				loser = player.user.username
		elif players.count() == 2:
			player1, player2 = players
			if player1.match_winner:
				winner = player1.user.username
				loser = player2.user.username
			else:
				winner = player2.user.username
				loser = player1.user.username
		else:
			return Response({"message": "Invalid number of players"}, status=status.HTTP_400_BAD_REQUEST)

		match_details = {
			'winner' : winner,
			'loser' : loser,
			'ball_max_speed' : match.ball_max_speed,
			'ball_contacts' : match.ball_contacts,
			'duration': match.duration
			}
		return Response(match_details, status=status.HTTP_200_OK)