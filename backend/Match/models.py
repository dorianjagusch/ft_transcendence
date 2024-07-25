from django.db import models
from datetime import datetime
from .matchState import MatchState
from Tournament.models import Tournament
class Match(models.Model):

	state = models.IntegerField(choices=MatchState.choices, default=MatchState.LOBBY)
	start_ts = models.DateTimeField(null=True, blank=True)
	end_ts = models.DateTimeField(null=True, blank=True)
	insert_ts = models.DateTimeField(auto_now_add=True)
	update_ts = models.DateTimeField(auto_now=True)
	ball_contacts = models.IntegerField(default=0)
	ball_max_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

	tournament = models.ForeignKey(Tournament, related_name='matches', null=True, blank=True, default=None, on_delete=models.CASCADE)

	def start_match(self):
		if self.state == MatchState.LOBBY:
			self.state = MatchState.IN_PROGRESS
			self.start_time = datetime.now()
			self.save()

	def finish_match(self):
		if self.state == MatchState.IN_PROGRESS:
			self.state = MatchState.FINISHED
			self.end_time = datetime.now()
			self.save()

	def abort_match(self):
		if self.state in [MatchState.LOBBY, MatchState.IN_PROGRESS]:
			self.state = MatchState.ABORTED
			self.end_time = datetime.now()
			self.save()

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Match {self.id} - {self.get_state_display()}'
