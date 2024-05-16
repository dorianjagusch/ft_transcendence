from django.db import models

from django.core.exceptions import ValidationError
from User.models import User

# Create your models here.
class Match(models.Model):
	player1_id = models.ForeignKey(User, related_name='player1_id', null=False, blank=False, on_delete=models.CASCADE)
	player2_id = models.ForeignKey(User, related_name='player2_id', null=False, blank=False, on_delete=models.CASCADE)
	
	player1_score = models.PositiveIntegerField(default=0)
	player2_score = models.PositiveIntegerField(default=0)

	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField()

	# for later
	# tournament_id = models.ForeignKey(Tournament, related_name='tournament_id', null=True, blank=True, on_delete=models.SET_NULL)
	# tournament_phase_id = models.ForeignKey(TournamentPhase, related_name='tournament_phase_id', null=True, blank=True, on_delete=models.SET_NULL)

	def clean(self):
		# Prevent a user from playing against themself
		if self.player1_id == self.player2_id:
			raise ValidationError('Players must be different.')
		
	class Meta:
		app_label = 'Match'