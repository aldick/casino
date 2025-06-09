from rest_framework import serializers
from game.serializers import BetSerializer


class CrashSerializer(BetSerializer):
    stop_value = serializers.DecimalField(max_digits=4, decimal_places=2)
    
    def validate_stop_value(self, stop_value):
        """
        Check that stop_value is not negative or equal to zero
        """
        if stop_value <= 0:
            raise serializers.ValidationError(
                "stop_value cannot be negative or zero"
            )
        return stop_value