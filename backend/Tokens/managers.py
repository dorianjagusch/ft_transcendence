from django.db import models

from .models import MatchToken
from User.models import User
from Match.models import Match

class MatchTokenManager(models.Manager):
	@staticmethod
	def create_match_token(user_left_side: User, user_right_side: User) -> MatchToken:
		match_token = MatchToken.objects.create(
			user_left_side=user_left_side,
			user_right_side=user_right_side
		)
		return match_token
	
	@staticmethod
	def create_single_match_token(host_user: User, guest_user: User) -> MatchToken:
		return MatchTokenManager.create_match_token(host_user, guest_user)

	@staticmethod
	def create_tournament_match_token(match: Match) -> MatchToken:
		players = match.players.all()
		return MatchTokenManager.create_match_token(players[0].user, players[1].user)
