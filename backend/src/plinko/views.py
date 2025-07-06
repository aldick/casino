import math
from decimal import Decimal
from random import choice

from rest_framework import status
from rest_framework.response import Response

from game.views import GameView
from .serializers import PlinkoSerializer


class PlinkoView(GameView):
    """
    Execute game logic for plinko game
    Expects field "lines"
    For GET method returns the indexes of bottom fields
    For POST method returns result as a list of turns of the ball for each line where -1 is left and 1 is right
    For example: [-1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1]
    """
    
    serializer_class = PlinkoSerializer
    
    @staticmethod
    def formula_of_normal_distribution(x): 
        return ((1 / (10000) * math.sqrt(2 * math.pi))) ** ((x ** 2) / 2)

    @staticmethod
    def get_bottom_fields(lines):
        fields = []
        if lines % 2 == 0:
            side = lines // 2
            for i in range(-side, side+1):
                fields.append(round(1 / PlinkoView.formula_of_normal_distribution(i/(side+1)) / 2, 1))
        else:
            side = lines // 2
            for i in range(-side-3, side-1):
                x = (i/(side+1)) + 0.5
                fields.append(round(1 / (PlinkoView.formula_of_normal_distribution(x)) / 2, 1))
        return fields

    def get(self, request, *args, **kwargs):
        lines = request.query_params.get('lines')

        try:
            lines = int(lines)
            if not (8 <= lines <= 16):
                return Response(
                    {"lines": "Lines must be between 8 and 16"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError):
            return Response(
                {"lines": "Lines must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bottom_fields = self.get_bottom_fields(lines)
        return Response(
            {"bottom_fields": bottom_fields},
            status=status.HTTP_200_OK
        )
    
    def play_game(self, bet, validated_data):
        lines = validated_data["lines"]
        
        result = []
        for _ in range(lines):
            result.append(choice([-1, 1]))
            
        result_place = sum(result) + lines // 2
        bottom_fields = PlinkoView.get_bottom_fields(lines)
        multiplier = Decimal(bottom_fields[result_place])
        
        return {
            "result": result,
            "payout": bet * multiplier
        }