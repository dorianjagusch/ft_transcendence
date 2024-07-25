from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Match
from Tokens.models import MatchToken
from Player.models import Player
from rest_framework import status
import sys

class MatchSetupManager:
	@staticmethod
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
			print(f"An error occurred: {e}", file=sys.stderr)
			return None

		return match

	def get_match_details(match_id : int):
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

		match_details = { 'winner' : winner, 'loser' : loser }
		return Response(match_details, status=status.HTTP_200_OK)

