from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
import plotly.io as pio
from django.http import HttpResponse
from .user_stats_table import UserTable
from .friend_stats_table import FriendsTable
from .mixins import UserTableMixin

class StatsView(APIView, UserTableMixin):	
	def get(self, request):
		user = request.user
		wins = self.get_wins_count(user)
		losses = self.get_losses_count(user)
		total_games_played = self.get_total_games_played_count(user)
		win_loss_ratio = self.get_win_loss_ratio(user)
		Winning_streak = self.get_win_streak_count(user)
		position_in_leaderboard = self.get_position_in_leaderboard(user)
		self.user_table = UserTable(user, wins, losses, total_games_played, win_loss_ratio, Winning_streak, position_in_leaderboard)
        # Create the Plotly figure
		fig = go.Figure(data=[go.Table(
			header=dict(values=['Statistic', 'Value']),
			cells=dict(values=[
				['Wins', 'Losses', 'Total Games Played', 'Win/Loss Ratio', 'Winning Streak', 'Position in Leaderboard'],
				[wins, losses, total_games_played, win_loss_ratio, Winning_streak, position_in_leaderboard]
			])
		)])		
	
		# Convert the Plotly figure to an SVG string
		svg_str = fig.to_image(format="svg").decode("utf-8")

		return HttpResponse(svg_str, content_type='image/svg+xml')
