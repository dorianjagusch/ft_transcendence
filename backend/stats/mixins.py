from User.models import User
from django.db.models import Count, Q
from Match.models import Match
from Match.matchState import MatchState

	
class UserTableMixin:
	def get_wins_count(self, user: User):
		total_wins_count = user.players.filter(match_winner=True, match__state=MatchState.FINISHED).count()
		return total_wins_count
	
	def get_losses_count(self, user: User):
		total_losses_count = user.players.filter(match_winner=False, match__state=MatchState.FINISHED).count()
		return total_losses_count
	
	def get_total_games_played_count(self, user : User):
		total_game_played = user.players.filter(match__state=MatchState.FINISHED).count()
		return total_game_played
	
	def get_win_loss_ratio(self, user : User):
		if self.get_total_games_played_count(user) == 0:
			return 1.0
		return self.get_wins_count(user) / self.get_total_games_played_count(user)
	
	def get_win_streak_count(self, user: User):
		win_streak = 0

		# Retrieve all matches for the given user where they have played and the match is finished
		matches = Match.objects.filter(players__user=user, state=MatchState.FINISHED).order_by('-end_ts')

		for match in matches:
			if match.players.filter(user=user).first().match_winner == True:
				win_streak += 1
			else:
				break

		return win_streak
	
	def get_users_with_most_wins(self):
		return  User.objects.filter(is_active=True).annotate(total_wins=Count('players', filter=Q(players__match_winner=True))).order_by('-total_wins')

	def get_position_in_leaderboard(self, user: User):
		users_with_most_wins = self.get_users_with_most_wins()
		for index, ranked_user in enumerate(users_with_most_wins):
			if ranked_user.id == user.id:
				return index + 1  # Positions are 1-based
		return None  # Return None if user is not found in the leaderboard
	
	def get_last_5_game_scores(self, user: User):
		last_5_matches = Match.objects.filter(players__user=user, state=MatchState.FINISHED).order_by('-end_ts')[:5]
		scores = []
		for match in last_5_matches:
			player_match = match.players.filter(user=user).first()
			scores.append({
				'match_id': match.id,
				'score': player_match.score,
				'win': player_match.match_winner
			})
		return scores
	