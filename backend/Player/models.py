from django.db import models

from User.models import User
from Match.models import Match

# Create your models here.
class Player(models.Model):
	user_id = models.ForeignKey(User, related_name='players', null=False, blank=False, on_delete=models.CASCADE)
	match_id = models.ForeignKey(Match, related_name='players', null=False, blank=False, on_delete=models.CASCADE)
	score = models.PositiveIntegerField(default=0)
	match_winner = models.BooleanField(default=False)

	class Meta:
		app_label = 'player'