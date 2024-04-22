from rest_framework import serializers
from .models import Friends

class FriendsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friends
		fields = ['id', 'user_id', 'friend_id', 'start_date_time']
