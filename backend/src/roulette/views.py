from rest_framework import status
from rest_framework.response import Response

from decimal import Decimal
from random import choice, randint

from game.views import GameView
from game.models import Game
from .serializers import RouletteSerializer

class RouletteView(GameView):
    serializer_class = RouletteSerializer
    
    def play_game(self, bet_data_list):
        """
        Execute game logic for coinflip game.
        Expects bet_type ('number', 'color', 'even_odd') in validated_data.
        """
        result = randint(0, 36)
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        
        total_payout = 0
        detailed_results = []
        
        for data in bet_data_list:
            bet = Decimal(data["bet"])
            bet_type = data["bet_type"]
            bet_value = data["bet_value"]
            
            payout = Decimal("0")
            
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
                    
            detailed_results.append({
                "bet": str(bet),
                "bet_type": bet_type,
                "bet_value": bet_value,
                "payout": str(payout),
                "is_win": payout > Decimal("0")
            })
            
            total_payout += payout
                
        return {
            "total_payout": total_payout,
            "result": result,
            "details": detailed_results
        }    
    
    def post(self, request):
        user = request.user
        data = request.data
        
        many = isinstance(data, list)
        
        serializer = self.serializer_class(
            data=data,
            many=many,
            context={"balance": user.balance}
        )
        
        if serializer.is_valid():
            bets = serializer.data
            total_bet = sum((Decimal(str(b["bet"])) for b in bets), Decimal("0"))
            if user.balance < total_bet:
                return Response(
                    {"balance": "Insufficient balance for all bets"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            game_result = self.play_game(bets)
            total_payout = game_result["total_payout"]
            result = game_result["result"]
            
            game = Game.objects.create(
                name="Roulette",
                user=user,
                bet=total_bet,
                payout=total_payout,
                result=result
            )
            game.save()
            
            user.balance -= total_bet
            user.balance += total_payout
            user.save()

            return Response({
                "result": result,
                "total_bet": total_bet,
                "total_payout": total_payout,
                "balance": user.balance,
                "bets": game_result["details"]
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)