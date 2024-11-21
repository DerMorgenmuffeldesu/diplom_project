from typing import Required
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        address = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, address=address)
        return user

    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
