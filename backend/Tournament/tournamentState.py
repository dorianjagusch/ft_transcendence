from django.db import models

class TournamentState(models.IntegerChoices):
	LOBBY = 0, 'lobby'
	IN_PROGRESS = 1, 'in-progress'
	FINISHED = 2, 'finished'
	ABORTED = 3, 'aborted'