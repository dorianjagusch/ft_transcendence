from rest_framework import serializers

from .models import Tournament
from Tokens.models import TournamentGuestToken

class TournamentOutputSerializer(serializers.ModelSerializer):
	state_display = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Tournament
		fields = [
			'id',
			'host_user',
			'custom_name',
			'state',
			'state_display',
			'player_amount',
			'tournament_winner',
			'start_time',
			'end_time',
			'updated_at'
			]
		
class TournamentCreationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = [
			  'host_user',
			  'custom_name',
			  'player_amount'
		]

	def create(self, validated_data):
		# Get the authenticated user from the request context
		host_user = self.context['request'].user
		
		# Set the host_user field in the validated data
		validated_data['host_user'] = host_user
		
		# Create and return the tournament object
		return Tournament.objects.create(**validated_data)


class FourPlayerTournamentCreationSerializer(serializers.ModelSerializer):
	tournament_guest_token_first = serializers.UUIDField(write_only=True)
	tournament_guest_token_second = serializers.UUIDField(write_only=True)
	tournament_guest_token_third = serializers.UUIDField(write_only=True)

	class Meta:
		model = Tournament
		fields = [
			'host_user',
			'custom_name',
			'player_amount',
			'tournament_guest_token_first',
			'tournament_guest_token_second',
			'tournament_guest_token_third'
		]
		read_only_fields = ['state', 'start_time', 'end_time', 'updated_at']

	def validate_tournament_guest_token(self, token, request):
		try:
			guest_token = TournamentGuestToken.objects.get(token=token)
		except TournamentGuestToken.DoesNotExist:
			raise serializers.ValidationError(f'Token {token} does not exist')

		if not guest_token.is_active:
			raise serializers.ValidationError(f'Token {token} is not active')
		if guest_token.is_expired():
			raise serializers.ValidationError(f'Token {token} is expired')
		if request.user != guest_token.host_user:
			raise serializers.ValidationError('You are not the host user for this token')
		
		return guest_token
	
	def validate_player_amount(self, value):
		if value not in [4, 8]:
			raise serializers.ValidationError("Player amount must be either 4 or 8.")
		return value

	def validate(self, data):
		data['tournament_guest_token_first'] = self.validate_tournament_guest_token(data['tournament_guest_token_first'])
		data['tournament_guest_token_second'] = self.validate_tournament_guest_token(data['tournament_guest_token_second'])
		data['tournament_guest_token_third'] = self.validate_tournament_guest_token(data['tournament_guest_token_third'])
		data['player_amount'] = self.validate_player_amount(data['player_amount'])
		return data

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['tournament_guest_token_first'] = str(instance.tournament_guest_token_first.token)
		representation['tournament_guest_token_second'] = str(instance.tournament_guest_token_second.token)
		representation['tournament_guest_token_third'] = str(instance.tournament_guest_token_third.token)
		return representation
	
class EightPlayerTournamentCreationSerializer(FourPlayerTournamentCreationSerializer):
	tournament_guest_token_fourth = serializers.UUIDField(write_only=True)
	tournament_guest_token_fifth = serializers.UUIDField(write_only=True)
	tournament_guest_token_sixth = serializers.UUIDField(write_only=True)
	tournament_guest_token_seventh = serializers.UUIDField(write_only=True)

	class Meta(FourPlayerTournamentCreationSerializer.Meta):
		fields = FourPlayerTournamentCreationSerializer.Meta.fields + [
			'tournament_guest_token_fourth',
			'tournament_guest_token_fifth',
			'tournament_guest_token_sixth',
			'tournament_guest_token_seventh'
		]

	def validate_player_amount(self, value):
		if value not in [8]:
			raise serializers.ValidationError("Player amount must be 8.")
		return value

	def validate(self, data):
		data = super().validate(data)
		data['tournament_guest_token_fourth'] = self.validate_tournament_guest_token(data['tournament_guest_token_fourth'])
		data['tournament_guest_token_fifth'] = self.validate_tournament_guest_token(data['tournament_guest_token_fifth'])
		data['tournament_guest_token_sixth'] = self.validate_tournament_guest_token(data['tournament_guest_token_sixth'])
		data['tournament_guest_token_seventh'] = self.validate_tournament_guest_token(data['tournament_guest_token_seventh'])
		data['player_amount'] = self.validate_player_amount(data['player_amount'])
		return data

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		guest_tokens = instance.guest_tokens.all()
		representation['tournament_guest_token_first'] = str(guest_tokens[0].token)
		representation['tournament_guest_token_second'] = str(guest_tokens[1].token)
		representation['tournament_guest_token_third'] = str(guest_tokens[2].token)
		representation['tournament_guest_token_fourth'] = str(guest_tokens[3].token)
		representation['tournament_guest_token_fifth'] = str(guest_tokens[4].token)
		representation['tournament_guest_token_sixth'] = str(guest_tokens[5].token)
		representation['tournament_guest_token_seventh'] = str(guest_tokens[6].token)
		return representation

