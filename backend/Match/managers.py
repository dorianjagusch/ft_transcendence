from django.db import models

from .models import Match
from Team.models import Team

class MatchManager(models.Manager):
	def get_match_teams(self, match_id):
		try:
			match = self.get(pk=match_id)
		except Match.DoesNotExist:
			raise ValueError("Match with id '{}' does not exist.".format(match_id))
		
		team_1 = Team.objects.get(pk=match.team_1_id)
		team_2 = Team.objects.get(pk=match.team_2_id)

		return team_1, team_2
	
	def get_matches_with_team(self, team_id):
		matches_with_team = self.filter(
            models.Q(team_1_id__in=team_id) | models.Q(team_2_id__in=team_id)
        )
		return matches_with_team

	def get_matches_with_user(self, user_id):
		teams_with_user = Team.objects.get_teams_with_user(user_id)
		matches_with_player_teams = self.filter(
            models.Q(team_1_id__in=teams_with_user) | models.Q(team_2_id__in=teams_with_user)
        )
		return matches_with_player_teams