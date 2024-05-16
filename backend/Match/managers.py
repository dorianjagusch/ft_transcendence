from django.db import models
from django.db.models import Q

from .models import Match
from .MatchStatus import MatchStatus
from User.models import User

class MatchManager(models.Manager):
	def get_match_players(self, match_id):
		try:
			match = self.get(pk=match_id)
		except Match.DoesNotExist:
			raise ValueError("Match with id '{}' does not exist.".format(match_id))
		
		player1 = User.objects.get(pk=match.player1_id)
		player2 = User.objects.get(pk=match.player2_id)

		return player1, player2
	
	def get_match_winner(self, match_id):
		try:
			match = self.get(pk=match_id)
		except Match.DoesNotExist:
			raise ValueError("Match with id '{}' does not exist.".format(match_id))
		
		if match.player1_score > match.player2_score:
			winner = User.objects.get(pk=match.player1_id)
		else:
			winner = User.objects.get(pk=match.player2_id)
		return winner

	def get_matches_with_user(self, user_id, match_status):
		try:
			user = User.objects.get(pk=user_id)
		except Match.DoesNotExist:
			raise ValueError("User with id '{}' does not exist.".format(user_id))
		matches_with_user = self.filter(
            models.Q(player1_id__in=user_id) | models.Q(player2_id__in=user_id)
        )
		matches_to_get = []
		if match_status == MatchStatus.WINS.value:
			matches_to_get = matches_with_user.filter(
					Q(player1_id=user_id, player1_score__gt=models.F('player2_score')) |
					Q(player2_id=user_id, player2_score__gt=models.F('player1_score'))
				)
		elif match_status == MatchStatus.LOSSES.value:
			matches_to_get = matches_with_user.filter(
					Q(player1_id=user_id, player1_score__lt=models.F('player2_score')) |
					Q(player2_id=user_id, player2_score__lt=models.F('player1_score'))
				)
		else:
			matches_to_get = matches_with_user
		return matches_to_get
