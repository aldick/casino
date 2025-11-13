from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

from .models import User

User = get_user_model()
        
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password', 'balance']
        extra_kwargs = {
            'password': {'write_only': True}  # Password is write-only
        }
