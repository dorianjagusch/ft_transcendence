from rest_framework import serializers
<<<<<<< Updated upstream
from .models import AbstractToken, MatchToken
=======
from .models import AbstractToken, MatchToken, TournamentToken

from django.contrib.auth import authenticate
>>>>>>> Stashed changes

class AbstractTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractToken
        fields = ['token']

class MatchTokenSerializer(AbstractTokenSerializer):
    class Meta(AbstractTokenSerializer.Meta):
<<<<<<< Updated upstream
        model = MatchToken
=======
        model = MatchToken
        fields = ['token']

class TournamentTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentToken
        fields = ['token']

class GuestUserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    custom_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('Both username and password are required')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        custom_name = validated_data.get('custom_name', None)
        
        host_user = self.context['host_user']
        
        token = TournamentGuestToken.objects.create(
            host_user=host_user,
            guest_user=user,
            custom_name = custom_name
        )
        
        return token
>>>>>>> Stashed changes
