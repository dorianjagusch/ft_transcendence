from rest_framework import serializers
from .models import Friend
from User.models import User

class FriendOutputSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	friend_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Friend
		fields = ['id', 'user_id', 'friend_id']

class FriendInputSerializer(serializers.ModelSerializer):
	friend_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Friend
		fields = ['id', 'friend_id']
