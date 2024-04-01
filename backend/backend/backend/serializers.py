from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'login']

		def update(self, instance, validated_data):
			instance.login = validated_data.get('login', instance.login)
			instance.save()
			return instance
