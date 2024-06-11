from django.db import models

class TournamentState(models.IntegerChoices):
	IN_PROGRESS = 0, 'in_progress'
	FINISHED = 1, 'finished'
	ABORTED = 2, 'aborted'