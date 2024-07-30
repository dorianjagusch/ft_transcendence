from django.db import models
from datetime import datetime
from .matchState import MatchState
from Tournament.models import Tournament
from django.utils import timezone
import sys

class Match(models.Model):
	state = models.IntegerField(choices=MatchState.choices, default=MatchState.LOBBY)
	start_ts = models.DateTimeField(null=True, blank=True, default=timezone.now)
	end_ts = models.DateTimeField(null=True, blank=True, default=timezone.now)
	insert_ts = models.DateTimeField(auto_now_add=True)
	update_ts = models.DateTimeField(auto_now=True)
	ball_contacts = models.IntegerField(default=0)
	ball_max_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	duration = models.CharField(max_length=15, default='00:00:00.000')

	tournament = models.ForeignKey(Tournament, related_name='matches', null=True, blank=True, default=None, on_delete=models.CASCADE)

	def start_match(self):
		if self.state == MatchState.LOBBY:
			self.state = MatchState.IN_PROGRESS
			self.start_time = datetime.now()
			self.save()

	def finish_match(self):
		if self.state == MatchState.IN_PROGRESS:
			self.state = MatchState.FINISHED
			self.end_ts = timezone.now()
			self.calculate_duration()
			self.save()

	def abort_match(self):
		if self.state in [MatchState.LOBBY, MatchState.IN_PROGRESS]:
			self.state = MatchState.ABORTED
			self.end_ts = timezone.now()
			self.calculate_duration()
			self.save()

	def calculate_duration(self):
		if self.start_ts and self.end_ts:
			if timezone.is_naive(self.start_ts):
				self.start_ts = timezone.make_aware(self.start_ts)
			if timezone.is_naive(self.end_ts):
				self.end_ts = timezone.make_aware(self.end_ts)
			duration_milliseconds = int((self.end_ts - self.start_ts).total_seconds() * 1000)
			self.duration = self.milliseconds_to_hms_milliseconds(duration_milliseconds)

	def milliseconds_to_hms_milliseconds(self, milliseconds):
		hours, remainder = divmod(milliseconds, 3600000)
		minutes, remainder = divmod(remainder, 60000)
		seconds, milliseconds = divmod(remainder, 1000)
		return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}'

	def seconds_to_hms(self, seconds):
		hours, remainder = divmod(seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

	def __str__(self):
		# The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
		return f'Match {self.id} - {self.get_state_display()}'
