import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import CoinFlipSerializer
from account.models import Profile

class CoinFlipView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = CoinFlipSerializer(data=request.data)

		if serializer.is_valid():
			user_choice = serializer.validated_data["choice"]
			bet = serializer.validated_data["bet"]

			flip_result = random.choice(["Heads", "Tails"])
			is_win = (user_choice == flip_result)

			profile = Profile.objects.get(user=request.user)
			if bet > profile.balance:
				return Response({
					"error": "Not enough money on balance"
				})
			if is_win:
				profile.balance += bet
			else:
				profile.balance -= bet
			profile.save()


			return Response({
				"flip_result": flip_result,
				"user_choice": user_choice,
				"bet": bet,
				"is_win": is_win,
				"message": "You won!" if is_win else "You lost!"
			})

		return Response(serializer.errors, status=400)
