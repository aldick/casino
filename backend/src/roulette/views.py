from random import choice, randint

from game.views import GameView
from .serializers import RouletteSerializer

class RouletteView(GameView):
    serializer_class = RouletteSerializer
    
    def play_game(self, bet, validated_data):
        """
        Execute game logic for coinflip game.
        Expects bet_type ('number', 'color', 'even_odd') in validated_data.
        """
        result = randint(0, 36)
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        
        bet_type = validated_data["bet_type"]
        bet_value = validated_data["bet_value"]
        
        payout = 0
        
        if bet_type == "number" and int(bet_value) == result:
            payout = 36 * bet
        if bet_type == "color":
            if bet_value == "red" and result in red_numbers:
                payout = 2 * bet
            if bet_value == "black" and result not in red_numbers:
                payout = 2 * bet
        if bet_type == "even_odd":
            if bet_value == "even" and result % 2 == 0:
                payout = 2 * bet
            if bet_value == "odd" and result % 2 != 0:
                payout = 2 * bet
                
        return {"payout": payout,
                "result": result}    
            