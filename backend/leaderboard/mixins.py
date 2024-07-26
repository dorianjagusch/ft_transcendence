from .leader_board_table import LeaderBoardTable
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from User.models import User

class LeaderBoardTableMixin:
	def leader_table_response(self):
			self.leader_table = LeaderBoardTable
			users_with_most_wins = User.objects.filter(is_active=True).annotate(
				total_wins=Count('players', filter=Q(players__match_winner=True))
			).order_by('-total_wins')

			self.leader_table.users = [user.username for user in users_with_most_wins]
			self.leader_table.wins = [user.total_wins for user in users_with_most_wins]

			stats = [{"user": user, "wins": wins, "place": index + 1} for index, (user, wins) in enumerate(zip(self.leader_table.users, self.leader_table.wins))]

			json_response_data = stats

			return Response(json_response_data, status=status.HTTP_200_OK)
