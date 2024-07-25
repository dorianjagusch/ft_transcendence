from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
import plotly.io as pio
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status

from .user_stats_table import UserTable
from .mixins import UserTableMixin
from User.models import User
from shared_utilities.decorators import must_be_authenticated

class StatsView(APIView, UserTableMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request, user_id):
		user = User.objects.filter(id = user_id).first()
		if not user:
			return Response({"message": "User was not found"}, status=status.HTTP_404_NOT_FOUND)
		wins = self.get_wins_count(user)
		losses = self.get_losses_count(user)
		total_games_played = self.get_total_games_played_count(user)
		win_loss_ratio = self.get_win_loss_ratio(user)
		winning_streak = self.get_win_streak_count(user)
		position_in_leaderboard = self.get_position_in_leaderboard(user)
		self.user_table = UserTable(user, wins, losses, total_games_played, win_loss_ratio, winning_streak, position_in_leaderboard)

		data = {
			'wins': wins,
			'losses': losses,
			'total_games_played': total_games_played,
			'win_loss_ratio': win_loss_ratio,
			'winning_streak': winning_streak,
			'position_in_leaderboard': position_in_leaderboard
		}

		return Response(data, status=status.HTTP_200_OK)

class StatsGraphView(APIView, UserTableMixin):
	@method_decorator(must_be_authenticated)
	def get (self, request, user_id):
		user = User.objects.filter(id = user_id).first()
		if not user:
			return Response({"message": "User was not found"}, status=status.HTTP_404_NOT_FOUND)
		wins = self.get_wins_count(user)
		losses = self.get_losses_count(user)
		total_games_played = self.get_total_games_played_count(user)
		# If no games are played, the whole circle will be gray
		if total_games_played == 0:
			labels = ['No Games Played']
			values = [1]
			colors = ['gray']
		else:
			labels = ['Wins', 'Losses']
			values = [wins, losses]
			colors = ['green', 'red']
		
		returnfig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.3  # This is optional, it creates a donut chart if > 0
        )])
		# Convert the Plotly figure to an SVG string
		svg_str = fig.to_image(format="svg").decode("utf-8")

		return HttpResponse(svg_str, content_type='image/svg+xml')