from rest_framework import serializers

from .models import Promocode


class DepositSerializer(serializers.Serializer):
    deposit = serializers.DecimalField(decimal_places=2, max_digits=20)
    
    def validate_deposit(self, deposit):
        if deposit <= 0:
            raise serializers.ValidationError("A deposit must be more than 0")
        return deposit


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = "__all__"
        
    def validate_name(self, value):
        return value.upper()
        
    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("end_date must be after stard_date")
        return data
    