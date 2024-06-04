from rest_framework import serializers

from .models import Tournament
from Tokens.models import TournamentGuestToken

class TournamentOutputSerializer(serializers.ModelSerializer):
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    player_amount = serializers.IntegerField(source='player_amount', read_only=True)

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
    tokens = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Tournament
        fields = [
            'host_user',
            'custom_name',
            'player_amount',
            'tokens'
        ]
        read_only_fields = ['state', 'start_time', 'end_time', 'updated_at']

    def validate_tournament_guest_token(self, token):
        try:
            guest_token = TournamentGuestToken.objects.get(token=token)
        except TournamentGuestToken.DoesNotExist:
            raise serializers.ValidationError(f'Token {token} does not exist')

        if not guest_token.is_active:
            raise serializers.ValidationError(f'Token {token} is not active')
        if guest_token.is_expired():
            raise serializers.ValidationError(f'Token {token} is expired')
        if self.context['request'].user != guest_token.host_user:
            raise serializers.ValidationError('You are not the host user for this token')
        
        return guest_token

    def validate_token_amount(self, tokens):
        tokens_amount = len(tokens)
        if tokens_amount not in [3, 7]:
            raise serializers.ValidationError("There must be 3 or 7 guest tokens.")
        
    def validate(self, data):
        guest_tokens = data.get('tokens')
        if not guest_tokens:
            raise serializers.ValidationError("No tokens in serializer.")

        self.validate_token_amount(guest_tokens)

        # Validate each token
        data['tokens'] = self.validate_tournament_guest_token(guest_tokens)
        return data


