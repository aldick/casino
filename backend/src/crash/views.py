from random import randint, choice
from decimal import Decimal

from .serializers import CrashSerializer
from game.views import GameView

class CrashView(GameView):
    serializer_class = CrashSerializer
    
    def play_game(self, bet, validated_data):
        """
        Execute game logic for crash game.
        Expects stop_value in validated_data
        """
        result = Decimal(choice(
            [
                randint(1, 150), 
                randint(1, 200),
                randint(1, 1000)
            ]
        ) / 100)
        
        payout = 0
        stop_value = validated_data["stop_value"]
        if stop_value <= result:
            payout = bet * stop_value

        return {"payout": payout,
                "result": result}