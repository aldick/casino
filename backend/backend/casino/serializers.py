from rest_framework import serializers


class CoinFlipSerializer(serializers.Serializer):
    bet = serializers.IntegerField(min_value=1)
    choice = serializers.ChoiceField(choices=["Heads", "Tails"])
