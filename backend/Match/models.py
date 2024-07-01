from django.db import models
from datetime import datetime

# Question to Meri: put into separate file?
class MatchState(models.IntegerChoices):
	LOBBY = 0, 'lobby'
	IN_PROGRESS = 1, 'in_progress'
	FINISHED = 2, 'finished'
	ABORTED = 3, 'aborted'


# Create your models here.
class Match(models.Model):
	state = models.IntegerField(choices=MatchState.choices, default=MatchState.LOBBY)
	start_time = models.DateTimeField(null=True, blank=True)
	end_time = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def start_match(self):
		if self.state == MatchState.LOBBY.value:
			self.state = MatchState.IN_PROGRESS.value
			self.start_time = datetime.now()
			self.save()

	def finish_match(self):
		if self.state == MatchState.IN_PROGRESS.value:
			self.state = MatchState.FINISHED.value
			self.end_time = datetime.now()
			self.save()

	def abort_match(self):
		if self.state in [MatchState.LOBBY.value, MatchState.IN_PROGRESS.value]:
			self.state = MatchState.ABORTED.value
			self.end_time = datetime.now()
			self.save()

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Match {self.id} - {self.get_state_display()}'

	# for later
	# tournament_id = models.ForeignKey(Tournament, related_name='tournament_id', null=True, blank=True, on_delete=models.SET_NULL)
	# tournament_phase_id = models.ForeignKey(TournamentPhase, related_name='tournament_phase_id', null=True, blank=True, on_delete=models.SET_NULL)

