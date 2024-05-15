from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from User.models import User
from backend.Team.managers import TeamManager

# Create your models here.
class Team(models.Model):
	team_name = models.CharField(_('team_name'), max_length=30, null=True, blank=True)
	team_member_1_id = models.ForeignKey(User, related_name='team_member_1_id', null=False, blank=False, on_delete=models.CASCADE)
	team_member_2_id = models.ForeignKey(User, related_name='team_member_2_id', null=True, blank=True, on_delete=models.SET_NULL)
	insertTS = models.DateTimeField(auto_now_add=True)

	objects = TeamManager()

	def __str__(self):
		return f"{self.team_name} - {self.team_member_1_id} - {self.team_member_2_id} - {self.insertTS}"
	
	def clean(self):
		# Prevent the same user from being both members in a team
		if self.team_member_1_id == self.team_member_2_id:
			raise ValidationError('Team members must be different users.')

	class Meta:
		app_label = 'Team'

		