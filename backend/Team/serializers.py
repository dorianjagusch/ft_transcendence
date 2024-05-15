from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Team
from User.models import User

class TeamSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	friend_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Team
		fields = ['id', 'team_name', 'team_member_1_id, team_member_2_id']