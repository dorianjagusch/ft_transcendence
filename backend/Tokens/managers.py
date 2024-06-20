from django.db import models, transaction

from Match.models import Match
from Tournament.exceptions import TournamentInProgressException

class MatchTokenManager(models.Manager):
	def create_single_match_token(self, host_user, guest_user):
		match_token = self.create(
			user_left_side=host_user,
			user_right_side=guest_user
		)
		return match_token

	def create_tournament_match_token_for_next_match(self, tournament):
		try:
			next_match = Match.objects.get(tournament_match_id=tournament.next_match)
		except Match.DoesNotExist:
			raise TournamentInProgressException(f"Cannot create match token for next tournament match because no match with tournament_match_id {tournament.next_match} (this should not happen!)")
		if next_match.players.count() < 2:
			raise TournamentInProgressException(f"Cannot create match token for next tournament match because not enough players for match with tournament_match_id {tournament.next_match} (this should not happen!)")
		match_token = self.create(
			user_left_side=next_match.players.all()[0].user,
			user_right_side=next_match.players.all()[1].user,
		)
		return match_token

class TournamentGuestTokenManager(models.Manager):
	def create_tournament_guest_token(self, host_user, guest_user):
		tournament_guest_token = self.create(
			host_user=host_user,
			guest_user=guest_user
		)
		return tournament_guest_token
