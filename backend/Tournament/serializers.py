from rest_framework import serializers

from .models import Tournament, \
						TournamentPlayer

class TournamentPlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = TournamentPlayer
		fields = ['id', 'user', 'name_in_tournament']

class TournamentCreationSerializer(serializers.ModelSerializer):
	host_user_display_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

	class Meta:
		model = Tournament
		fields = [
			'name',
			'host_user',
			'host_user_display_name',
			'player_amount',
		]
	
	def validate_custom_name(self, custom_name: str) -> str:
		if custom_name == '':
			raise serializers.ValidationError("This field may not be blank.")
		if len(custom_name) > 30:
			raise serializers.ValidationError("Ensure this field has no more than 30 characters.")
		return custom_name
	
	def validate_tournament_player_amount(self, player_amount: int) -> None:
		if player_amount not in [4, 8]:
			raise serializers.ValidationError("Must have 4 or 8 players.")
		
	def validate(self, data):
		tournament_name = data.get('name')
		if tournament_name:
			self.validate_custom_name(tournament_name)

		host_user_display_name = data.get('host_user_display_name')
		if host_user_display_name:
			self.validate_custom_name(host_user_display_name)
		
		self.validate_tournament_player_amount(data.get('player_amount'))

		return data