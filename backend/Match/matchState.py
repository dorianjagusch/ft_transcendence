from django.db import models

class MatchState(models.IntegerChoices):
	LOBBY = 0, 'lobby'
	IN_PROGRESS = 1, 'in_progress'
	FINISHED = 2, 'finished'
	ABORTED = 3, 'aborted'