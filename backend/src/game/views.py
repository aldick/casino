from random import choice, randint
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Profile
from .models import Game
from .serializers import BetSerializer


class GameView(APIView):
    serializer_class = BetSerializer
    
    def play_game(self, bet, validated_data):
        """
        Execute the game logic and returns the payout and result.
        Must be implemented in child classes.
        """
        raise NotImplementedError("Subclasses must implement play_game()")
    
    def get(self, request):
        """
        Returns last 20 games played by user
        """
        games = Game.objects.filter(user=request.user,
                                    name=self.__class__.__name__[:-4])[:20]
        print(self.__class__.__name__[:-4], request.user)
        response = dict()
        for game in games:
            response[game.id] = {
                "bet": game.bet,
                "is_win": game.is_win,
                "payout": game.payout,
                "result":  game.result
            }
        return Response(response)

    def post(self, request):
        user = request.user  
        
        serializer = self.serializer_class(
            data=request.data,
            context={
                "balance": user.profile.balance,
            }
        )
        
        if serializer.is_valid():
            bet = serializer.validated_data["bet"]
            
            game = self.play_game(bet, serializer.validated_data)
            payout = game["payout"]
            result = game["result"]
            
            game = Game.objects.create(
                name = f"{self.__class__.__name__}"[:-4],
                user = request.user,
                bet = bet,
                payout = payout,
                result = result
            )
            game.save()
            
            user.profile.balance -= bet
            user.profile.balance += payout
            user.profile.save()
            
            return Response(
                {
                    **serializer.data,
                    "is_win": True if payout > 0 else False,
                    "payout": payout,
                    "result": result
                },
                status=status.HTTP_200_OK
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
            