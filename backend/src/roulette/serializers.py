from rest_framework import serializers
from game.serializers import BetSerializer


class RouletteSerializer(BetSerializer):
    bet_type = serializers.ChoiceField(choices=["color", "even_odd", "number"])
    bet_value = serializers.CharField(max_length=10)
    
    def validate(self, data):
        """
        Validate bet_type and bet_value for the roulette
        """
        data = super().validate(data)
        bet_type = data.get("bet_type")
        bet_value = data.get("bet_value")
        
        if bet_type == "number":
            try:
                number = int(bet_value)
                if not (0 <= number <= 36):
                    raise serializers.ValidationError({
						"bet_value": "Number must be between 0 and 36"
					})
            except ValueError:
                raise serializers.ValidationError({
					"bet_value": "Number must be a valid integer"
				})
        elif bet_type == "color" and bet_value not in ("red", "black"):
            raise serializers.ValidationError({
				"bet_value": "Color must be 'red' or 'black'"
			})
        elif bet_type == "even_odd" and bet_value not in ("even", "odd"):
            raise serializers.ValidationError({
				"bet_value": "Must be 'even' or 'odd'"
			}) 
            
        return data  