from random import choice
from django.http import JsonResponse

from game.views import GameView
from .serializers import CoinFlipSerializer

class CoinFlipView(GameView):
    serializer_class = CoinFlipSerializer
    
    def play_game(self, bet, validated_data):
        """
        Execute game logic for coinflip game.
        Expects choice ('heads', 'tails') in validated_data.
        """
        user_choice = validated_data["choice"]
        result = choice(["heads", "tails"])
        payout = bet * 2 if user_choice == result else 0

        return {"payout": payout,
                "result": result}