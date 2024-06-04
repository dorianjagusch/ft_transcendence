from django.db import models
from datetime import datetime

from User.models import User
from .managers import TournamentManager

class TournamentState(models.IntegerChoices):
	IN_PROGRESS = 0, 'in_progress'
	FINISHED = 1, 'finished'
	ABORTED = 2, 'aborted'

# Create your models here.
class Tournament(models.Model):
	host_user = tournament_winner = models.ForeignKey(User, related_name='tournament_hosts', on_delete=models.CASCADE)
	custom_name = models.CharField(max_length=30, null=True, blank=True, default=None)
	state = models.IntegerField(choices=TournamentState.choices, default=TournamentState.IN_PROGRESS)
	player_amount = models.IntegerField(null=True, blank=True)
	tournament_winner = models.ForeignKey(User, related_name='tournament_winners', on_delete=models.CASCADE, null=True, blank=True)

	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TournamentManager()

	def finish_tournament(self):
		if self.state == TournamentState.IN_PROGRESS.value:
			self.state = TournamentState.FINISHED.value
			self.end_time = datetime.now()
			self.save()

	def abort_tournament(self):
		if self.state in TournamentState.IN_PROGRESS.value:
			self.state = TournamentState.ABORTED.value
			self.end_time = datetime.now()
			self.save()

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Tournament {self.pk} - {self.get_state_display()}'

