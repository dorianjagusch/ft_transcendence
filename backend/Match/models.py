from django.db import models
from datetime import datetime
from .matchState import MatchState
from Tournament.models import Tournament
from .playerMatchStatus import PlayerMatchStatus
class Match(models.Model):
    state = models.IntegerField(choices=MatchState.choices, default=MatchState.LOBBY)
    start_ts = models.DateTimeField(null=True, blank=True)
    end_ts = models.DateTimeField(null=True, blank=True)
    insert_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    tournament = models.ForeignKey(Tournament, related_name='matches', null=True, blank=True, default=None, on_delete=models.CASCADE)

    player_match_status = models.CharField(
        max_length=10,
        choices=PlayerMatchStatus.choices(),
        default=PlayerMatchStatus.NONE.value
    )
    
    def start_match(self):
        if self.state == MatchState.LOBBY.value:
            self.state = MatchState.IN_PROGRESS.value
            self.start_ts = datetime.now()
            self.save()

    def finish_match(self):
        if self.state == MatchState.IN_PROGRESS.value:
            self.state = MatchState.FINISHED.value
            self.end_ts = datetime.now()
            self.save()

    def abort_match(self):
        if self.state in [MatchState.LOBBY.value, MatchState.IN_PROGRESS.value]:
            self.state = MatchState.ABORTED.value
            self.end_ts = datetime.now()
            self.save()

    def __str__(self):
        # The method to retrieve the human-readable representation of an IntegerChoices enumeration is get_FOO_display(), where FOO is the name of the field.
        return f'Match {self.id} - {self.get_state_display()}'
