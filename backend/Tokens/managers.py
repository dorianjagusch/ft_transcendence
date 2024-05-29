from django.db import models

class MatchTokenManager(models.Manager):
	def create_match_token(self, user_left_side, user_right_side):
		match_token = self.create(
			user_left_side=user_left_side,
			user_right_side=user_right_side
		)
		return match_token
	
	def create_local_single_match_token(self, host_user, guest_user):
		return self.create_match_token(host_user, guest_user)
	
	def create_test_match_token(self, host_user):
		test_match_token = self.create_match_token(host_user, host_user)
		test_match_token.test_match = True
		return test_match_token
	
