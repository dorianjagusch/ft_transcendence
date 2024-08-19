from django.db import models

from User.models import User

class Player(models.Model):
	user = models.ForeignKey(User, related_name='players', null=False, blank=False, on_delete=models.CASCADE)
	match = models.ForeignKey('Match.Match', related_name='players', null=False, blank=False, on_delete=models.CASCADE) # lazy reference used for match model to avoid dependency issues
	score = models.PositiveIntegerField(default=0)
	match_winner = models.BooleanField(default=False)