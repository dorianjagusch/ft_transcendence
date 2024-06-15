from django.db import models

from User.models import User

# Create your models here.
class Player(models.Model):
	user = models.ForeignKey(User, related_name='players', null=False, blank=False, on_delete=models.CASCADE)
	# lazy reference used for match model to avoid dependency issues
	match = models.ForeignKey('Match.Match', related_name='players', null=False, blank=False, on_delete=models.CASCADE)
	score = models.PositiveIntegerField(default=0)
	match_winner = models.BooleanField(default=False)