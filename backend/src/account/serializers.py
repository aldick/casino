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
        fields = ['id', 'email', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}  # Password is write-only
        }
        read_only_fields = ['profile']
        
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError({
                "email": "A user with this email already exists."
            })
        return value
    
    def validate_username(self, value):
        if len(value) < 3:  # Example: Enforce minimum length
            raise serializers.ValidationError({
                "username": "Username must be at least 3 characters long."
            })
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError({
                "username": "A user with this username already exists."
            })
        return value
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class DepositSerializer(serializers.Serializer):
    deposit = serializers.DecimalField(decimal_places=2, max_digits=20)
    
    def validate_deposit(self, deposit):
        if deposit <= 0:
            raise serializers.ValidationError("A deposit must be more than 0")
        return deposit
