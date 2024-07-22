import plotly.io as pio
from User.models import User
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from Match.models import Match
from Match.matchState import MatchState
from Match.playerMatchStatus import PlayerMatchStatus
from .leader_board_table import LeaderBoardTable
from rest_framework.response import Response
from rest_framework import status
	
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
		current_streak = 0

		# Retrieve all matches for the given user where they have played and the match is finished
		matches = Match.objects.filter(players__user=user, state=MatchState.FINISHED).order_by('-end_ts')

		for match in matches:
			if match.player_match_status == PlayerMatchStatus.WINS.value:
				current_streak += 1
				win_streak = max(win_streak, current_streak)
			else:
				current_streak = 0

		return win_streak
	
	def get_users_with_most_wins(self):
		return  User.objects.annotate(total_wins=Count('players', filter=Q(players__match_winner=True))).order_by('-total_wins')

	def get_position_in_leaderboard(self, user: User):
		users_with_most_wins = self.get_users_with_most_wins()
		for index, ranked_user in enumerate(users_with_most_wins):
			if ranked_user.id == user.id:
				return index + 1  # Positions are 1-based
		return None  # Return None if user is not found in the leaderboard
	
	def leader_table_response(self):
		self.leader_table = LeaderBoardTable
		users_with_most_wins = User.objects.annotate(
			total_wins=Count('players', filter=Q(players__match_winner=True))
		).order_by('-total_wins')

		self.leader_table.users = [user.username for user in users_with_most_wins]
		self.leader_table.wins = [user.total_wins for user in users_with_most_wins]

		stats = [{"user": user, "wins": wins} for user, wins in zip(self.leader_table.users, self.leader_table.wins)]

		json_response_data = {
			"stats": stats
		}

		return Response(json_response_data, status=status.HTTP_200_OK)
