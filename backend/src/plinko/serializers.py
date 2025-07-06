from rest_framework import serializers
from game.serializers import BetSerializer


class PlinkoSerializer(BetSerializer):
    lines = serializers.IntegerField()
    
    def validate_lines(self, lines):
        if not (8 <= lines <= 16):
            raise serializers.ValidationError("Lines must be between 8 and 16")
        return lines

