from django.db import models, transaction

class MatchTokenManager(models.Manager):
	def create_single_match_token(self, host_user, guest_user):
		match_token = self.create(
			user_left_side=host_user,
			user_right_side=guest_user
		)
		return match_token
	
	def create_tournament_match_token(self, tournament_matchup):
		match_token = self.create(
			user_left_side=tournament_matchup.participant_left_side.user,
			user_right_side=tournament_matchup.participant_right_side.user,
			tournament_matchup = tournament_matchup
		)
		return match_token

class TournamentGuestTokenManager(models.Manager):
	def create_tournament_guest_token(self, host_user, guest_user):
		tournament_guest_token = self.create(
			host_user=host_user,
			guest_user=guest_user
		)
		return tournament_guest_token
