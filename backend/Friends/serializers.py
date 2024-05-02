from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Friends
from User.models import User

# rm later
import sys

class FriendsSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	friend_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Friends
		fields = ['id', 'user_id', 'friend_id']
