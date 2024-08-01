from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
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
		user = User.objects.filter(id = user_id, is_active=True).first()
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
		if total_games_played == 0:
			labels = ['No Games Played']
			values = [1]
			colors = ['gray']
		else:
			labels = ['Wins', 'Losses']
			values = [wins, losses]
			colors = ['green', 'red']
		
		fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.3  # This creates a donut chart
        )])
		svg_str = fig.to_image(format="svg").decode("utf-8")

		return HttpResponse(svg_str, content_type='image/svg+xml')
	
class MatchScoreGraphView(APIView, UserTableMixin):
	@method_decorator(must_be_authenticated)
	def get (self, request, user_id):
		user = User.objects.filter(id = user_id).first()
		if not user:
			return Response({"message": "User was not found"}, status=status.HTTP_404_NOT_FOUND)
		scores = self.get_last_5_game_scores(user)
		match_ids = [score['match_id'] for score in scores]
		match_scores = [0.2 if score['score'] == 0 else score['score'] for score in scores]
		match_colors = ['green' if score['win'] else 'red' for score in scores]
		match_texts = ['0' if score['score'] == 0 else str(score['score']) for score in scores]

		
		fig = go.Figure(data=[go.Bar(
			x=match_ids,
			y=match_scores,
			marker_color=match_colors,
			text=match_texts, 
            textposition='inside',
		)])

		fig.update_layout(
			title='Last 5 Match Scores',
			xaxis_title='Match ID',
			yaxis_title='Score',
			xaxis=dict(showticklabels=False),
			yaxis=dict(showticklabels=False)
		)

		svg_str = fig.to_image(format="svg").decode("utf-8")

		return HttpResponse(svg_str, content_type='image/svg+xml')