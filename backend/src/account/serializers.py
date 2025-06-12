from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['balance']
        
class CustomUserSerializer(UserSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'profile']
        
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError({
                "email": "A user with this email already exists."
            })
        return value
    
class DepositSerializer(serializers.Serializer):
    deposit = serializers.DecimalField(decimal_places=2, max_digits=10)
    
    def validate_deposit(self, deposit):
        if deposit <= 0:
            raise serializers.ValidationError("A deposit must be more than 0")
        return deposit
