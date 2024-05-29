from django.db import models

class MatchTokenManager(models.Manager):
	def create_match_token(self, user_left_side, user_right_side):
		match_token = self.create(
			user_left_side=user_left_side,
			user_right_side=user_right_side
		)
		return match_token
	
	def create_single_match_token(self, host_user, guest_user):
		return self.create_match_token(host_user, guest_user)

	# general concept for creating match tokens for tournaments
	def create_tournament_match_token(self, user_left_side, user_right_side, tournament_id, tournament_match_id):
		match_token = self.create_match_token(user_left_side, user_right_side)
		match_token.tournament_id = tournament_id
		match_token.tournament_match_id = tournament_match_id
	
