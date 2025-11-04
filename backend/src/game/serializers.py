from rest_framework import serializers


class BetSerializer(serializers.Serializer):
    bet = serializers.DecimalField(max_digits=20,
                                   decimal_places=2)
    
    def validate_bet(self, bet):
        """
        Check that bet is not negative
        """
        if bet < 0:
            raise serializers.ValidationError("Bet cannot be negative")
        return bet
    
    def validate(self, data):
        """
        Check that the balance is enough for the bet.
        """
        balance = self.context.get("balance")
        bet = data.get("bet")

        if balance < bet:
            raise serializers.ValidationError(
                {"balance": "Current balance is not enough"}
            )

        return data