import plotly.io as pio
from User.models import User
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from Match.models import Match
from Match.matchState import MatchState
from Match.playerMatchStatus import PlayerMatchStatus
	
class UserTableMixin:
	def get_wins_count(self, user: User):
		total_wins_count = user.players.filter(match_winner=True, match__state=MatchState.FINISHED).count()
		return total_wins_count
	
	def get_losses_count(self, user: User):
		total_losses_count = user.players.filter(match_winner=False, match__state=MatchState.FINISHED).count()
		return total_losses_count
	
	def get_total_games_played_count(self, user : User):
		total_game_played_count = user.players.filter(match__state=MatchState.FINISHED).count()
		return total_game_played_count
	
	def get_win_loss_ratio(self, user : User):
		if self.get_total_games_played_count(user) == 0:
			return 1.0
		return self.get_wins_count(user) / self.get_total_games_played_count(user)
	
	def get_win_streak_count(self, user: User):
		win_streak = 0
		current_streak = 0

		# Query for matches where the player won
		matches = Match.objects.filter(player_match_status=PlayerMatchStatus.WINS.value, end_ts__isnull=False).order_by('-end_ts')

		for match in matches:
			# Increment the streak if the match ended within the expected time frame
			if current_streak == 0 or (timezone.now() - match.end_ts <= timedelta(days=1)):
				current_streak += 1
			else:
				current_streak = 1
			win_streak = max(win_streak, current_streak)

		return win_streak

		return win_streak
	
	def get_users_with_most_wins(self):
		return  User.objects.annotate(total_wins=Count('players', filter=Q(players__match_winner=True))).order_by('-total_wins')

	def get_position_in_leaderboard(self, user: User):
		users_with_most_wins = self.get_users_with_most_wins()
		for index, ranked_user in enumerate(users_with_most_wins):
			if ranked_user.id == user.id:
				return index + 1  # Positions are 1-based
		return None  # Return None if user is not found in the leaderboard
