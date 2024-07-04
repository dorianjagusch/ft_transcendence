from django.db import models
from django.utils import timezone

from User.models import User
from .tournamentState import TournamentState

# Create your models here.
class Tournament(models.Model):
	host_user = models.ForeignKey(User, related_name='tournament_hosts', on_delete=models.SET_NULL)
	name = models.CharField(max_length=30, null=True, blank=True, default=None)
	state = models.IntegerField(choices=TournamentState.choices, default=TournamentState.LOBBY)
	next_match = models.IntegerField(default=0)
	player_amount = models.PositiveIntegerField(null=False, blank=False)
	winner = models.ForeignKey(User, related_name='tournament_winners', on_delete=models.SET_NULL, null=True, blank=True, default=None)

	insert_ts = models.DateTimeField(auto_now_add=True)
	start_ts = models.DateTimeField(null=True, blank=True)
	end_ts = models.DateTimeField(null=True, blank=True)
	update_ts = models.DateTimeField(auto_now=True)

	expire_ts = models.DateTimeField(null=True, blank=True)

	def start_tournament(self):
		if self.state == TournamentState.LOBBY.value:
			self.state = TournamentState.IN_PROGRESS.value
			self.start_ts = timezone.now()
			self.save()

	def finish_tournament(self):
		if self.state == TournamentState.IN_PROGRESS.value:
			self.state = TournamentState.FINISHED.value
			self.end_ts = timezone.now()
			self.save()

	def abort_tournament(self):
		if self.state in (TournamentState.LOBBY, TournamentState.IN_PROGRESS.value):
			self.state = TournamentState.ABORTED.value
			self.end_ts = timezone.now()
			self.save()

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Tournament {self.pk} - {self.get_state_display()}'
	
class TournamentPlayer(models.Model):
	tournament = models.ForeignKey(Tournament, related_name='players', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='tournament_players', on_delete=models.SET_NULL)
	display_name = models.CharField(max_length=30, null=True, blank=True, default=None)

	class Meta:
		unique_together = ('tournament', 'user')

