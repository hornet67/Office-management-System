from rest_framework import serializers
from .models import PendingUser, User_info

# Serializer for PendingUser registration
class PendingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingUser
        fields = ['name', 'email', 'phone_number', 'gender', 'role', 'company', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # hide password in API response
        }

# Serializer for active User_info (login)
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_info
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # hide password in API response
        }
