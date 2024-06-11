from django.db import models
from datetime import datetime

from User.models import User
from .managers import TournamentManager
from .tournamentState import TournamentState

# Create your models here.
class Tournament(models.Model):
	host_user = models.ForeignKey(User, related_name='tournament_hosts', on_delete=models.CASCADE)
	custom_name = models.CharField(max_length=30, null=True, blank=True, default=None)
	state = models.IntegerField(choices=TournamentState.choices, default=TournamentState.IN_PROGRESS)
	next_match = models.IntegerField(default=0)
	player_amount = models.IntegerField(null=True, blank=True)
	winner = models.ForeignKey(User, related_name='tournament_winners', on_delete=models.CASCADE, null=True, blank=True, default=None)

	insert_ts = models.DateTimeField(auto_now_add=True)
	start_ts = models.DateTimeField(null=True, blank=True)
	end_ts = models.DateTimeField(null=True, blank=True)
	updated_ts = models.DateTimeField(auto_now=True)

	objects = TournamentManager()

	def finish_tournament(self):
		if self.state == TournamentState.IN_PROGRESS.value:
			self.state = TournamentState.FINISHED.value
			self.end_ts = datetime.now()
			self.save()

	def abort_tournament(self):
		if self.state == TournamentState.IN_PROGRESS.value:
			self.state = TournamentState.ABORTED.value
			self.end_ts = datetime.now()
			self.save()

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Tournament {self.pk} - {self.get_state_display()}'
	
class TournamentParticipant(models.Model):
	tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='tournament_participants', on_delete=models.CASCADE)
	name_in_tournament = models.CharField(max_length=30, null=False, blank=False)

	class Meta:
		unique_together = ('tournament', 'user')

class TournamentMatchup(models.Model):
	tournament = models.ForeignKey(Tournament, related_name='matchups', on_delete=models.CASCADE)
	participant_left_side = models.ForeignKey(TournamentParticipant, related_name='matchups_as_participant_left_side', null=True, blank=True, on_delete=models.CASCADE)
	participant_right_side = models.ForeignKey(TournamentParticipant, related_name='matchups_as_participant_right_side', null=True, blank=True, on_delete=models.CASCADE)
	tournament_match_id = models.PositiveIntegerField() # do not mixup with Match model's id!
	winner = models.ForeignKey(TournamentParticipant, related_name='won_matchups', on_delete=models.CASCADE, null=True, blank=True)

	insert_ts = models.DateTimeField(auto_now_add=True)
	updated_ts = models.DateTimeField(auto_now=True)


	def __str__(self):
		return f'Match {self.tournament_match_id}: {self.participant_left_side.name_in_tournament} vs {self.participant_right_side.name_in_tournament}'

	class Meta:
		unique_together = ('tournament', 'tournament_match_id')
		ordering = ['tournament_match_id']
