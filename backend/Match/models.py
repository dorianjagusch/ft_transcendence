from django.db import models

from django.core.exceptions import ValidationError
from Team.models import Team

# Create your models here.
class Match(models.Model):
	team_1_id = models.ForeignKey(Team, related_name='Team_1_id', null=False, blank=False, on_delete=models.CASCADE)
	team_2_id = models.ForeignKey(Team, related_name='Team_2_id', null=False, blank=False, on_delete=models.CASCADE)
	
	team_1_member_1_score = models.PositiveIntegerField(default=0)
	team_1_member_2_score = models.PositiveIntegerField(default=0)

	team_2_member_1_score = models.PositiveIntegerField(default=0)
	team_2_member_2_score = models.PositiveIntegerField(default=0)

	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	aborted = models.BooleanField(default=False)

	# for later
	# tournament_id = models.ForeignKey(Tournament, related_name='tournament_id', null=True, blank=True, on_delete=models.SET_NULL)
	# tournament_phase_id = models.ForeignKey(TournamentPhase, related_name='tournament_phase_id', null=True, blank=True, on_delete=models.SET_NULL)

	def clean(self):
		# Prevent a team from playing against itself
		if self.team_1_id == self.team_2_id:
			raise ValidationError('Teams must be different.')
		
		# Prevent different teams from having the same member in them
		team_1_members = [self.team_1_id.team_member_1_id, self.team_1_id.team_member_2_id]
		team_2_members = [self.team_2_id.team_member_1_id, self.team_2_id.team_member_2_id]
		for member in team_1_members:
			if member and member in team_2_members:
				raise ValidationError(_('Teams cannot have the same members.'))
		
	class Meta:
		app_label = 'Match'