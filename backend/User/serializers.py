from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_superuser']



# This Serializer is used to check that a the given user data in a request body is valid
# (this cannot be done with the ModelSerializer as giving an existing user's data will cause an error because of unique constraits)
class CheckExistingUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, required=False)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)
    date_created = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)

    def validate(self, data):
        # Check if the user exists and if the password is correct
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")
        
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid username or password")
        
        # Compare each provided field with the corresponding field of the user object
        for key, value in data.items():
            if key not in self.fields:
                raise serializers.ValidationError(f"Unexpected field: {key}")
            if key == 'password':
                continue  # Skip password comparison as it has been already checked
            if getattr(user, key) != value:
                raise serializers.ValidationError(f"Field '{key}' does not match the user's data")
        
        return data