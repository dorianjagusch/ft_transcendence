from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
import plotly.io as pio
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from User.models import User


class StatsView(APIView):
	def get(self, request):
		x = [1, 2, 3, 4, 5]
		y = [10, 11, 12, 13, 14]
		fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ])

        # Convert plot to HTML
		plot_html = pio.to_html(fig, full_html=True)


		return HttpResponse(plot_html, content_type='text/html')
	
class LeaderBoardView(APIView):
	def get(self, request):
		users_with_most_wins = User.objects.annotate(total_wins=Count('players', filter=Q(players__match_winner=True))).order_by('-total_wins')
		
		header = ['Username', 'Total Wins']
		cells = [
            [user.username for user in users_with_most_wins],
            [user.total_wins for user in users_with_most_wins]
        ]

        # Create Plotly table figure
		fig = go.Figure(data=[go.Table(header=dict(values=header),
                                       cells=dict(values=cells))])

        # Convert plot to HTML
		plot_html = pio.to_html(fig, full_html=True)
		full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Leaderboard</title>
        </head>
        <body>
            <h1>Leaderboard</h1>
            <div>{plot_html}</div>
        </body>
        </html>
        """

		return HttpResponse(full_html, content_type='text/html')