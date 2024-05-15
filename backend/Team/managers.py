from django.db import models

from .models import Team
from User.models import User

class TeamManager(models.Manager):
	def get_team_members(self, team_id):
		try:
			team = self.get(pk=team_id)
		except Team.DoesNotExist:
			raise ValueError("Team with id '{}' does not exist.".format(team_id))

		member_1 = User.objects.get(pk=team.team_member_1_id)

		if team.team_member_2_id is None:
			return member_1
		else:
			member_2 = User.objects.get(pk=team.team_member_2_id)
			return member_1, member_2

	def get_teams_with_user(self, user_id):
		teams_with_user = self.filter(
            models.Q(team_member_1_id=user_id) | models.Q(team_member_2_id=user_id)
        )
		return teams_with_user

