from rest_framework import serializers
from game.serializers import BetSerializer


class CoinFlipSerializer(BetSerializer):
    choice = serializers.ChoiceField(choices=["heads", "tails"])
    