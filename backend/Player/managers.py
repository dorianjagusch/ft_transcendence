from django.db import models
from django.db.models import Q
from rest_framework.serializers import ValidationError

from .serializers import PlayerSerializer

class PlayerManager(models.Manager):
	def create_player(self, player_serializer_data):
		serializer = PlayerSerializer(data=player_serializer_data)

		if serializer.is_valid():
			player_instance = serializer.save()
			return player_instance
		else:
			raise ValidationError(serializer.errors)
		

	def get_player_match_opponent(self, player_id):
		try:
			player = self.get(pk=player_id)
		except models.DoesNotExist:
			raise ValueError("Player with id '{}' does not exist.".format(player_id))
		
		match = player.match
		opponent = self.filter(match=match).exclude(id=player_id)

		return opponent