from django.db import models
from User.models import User

# not used anywhere, delete later
class MatchTokenManager(models.Manager):
	def create_match_token(self, user_left_side: User, user_right_side: User) -> 'MatchToken':
		match_token = self.create(
			user_left_side=user_left_side,
			user_right_side=user_right_side
		)
		return match_token
	
	def create_single_match_token(self, host_user: User, guest_user: User) -> 'MatchToken':
		return self.create_match_token(host_user, guest_user)


	# CONCEPT FOR CREATING TOURNAMENT MATCH TOKENS
	# def create_tournament_match_token(self, user_left_side, user_right_side, tournament_id, tournament_match_id):
	# 	match_token = self.create_match_token(user_left_side, user_right_side)
	# 	match_token.tournament_id = tournament_id
	# 	match_token.tournament_match_id = tournament_match_id
	
