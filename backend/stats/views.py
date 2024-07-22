from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
import plotly.io as pio
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from User.models import User
from .user_stats_table import UserTable
from .leader_board_table import LeaderBoardTable
from .friend_stats_table import FriendsTable

from .mixins import UserTableMixin
from rest_framework.response import Response

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

class LeaderBoardView(APIView, UserTableMixin):
	def __init__(self):
		self.leader_table = LeaderBoardTable
        
	def get(self, request):
		# Queryset to get users with most wins
		users_with_most_wins = User.objects.annotate(
			total_wins=Count('players', filter=Q(players__match_winner=True))
		).order_by('-total_wins')

		# Set the users and wins attributes
		self.leader_table.users = [user.username for user in users_with_most_wins]
		self.leader_table.wins = [user.total_wins for user in users_with_most_wins]

		stats = [{"user": user, "wins": wins} for user, wins in zip(self.leader_table.users, self.leader_table.wins)]

		json_response_data = {
			"stats": stats
		}

		return Response(json_response_data, status=status.HTTP_200_OK)

