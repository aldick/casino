from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import DepositSerializer


class DepositView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "balance": request.user.profile.balance
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        
        if serializer.is_valid():
            deposit = serializer.validated_data["deposit"]
            profile = request.user.profile
                        
            profile.balance += deposit
            profile.save()
            
            return Response(
                {
                    "balance": "Successful replenishment of the balance",
                    "deposit": deposit,
                    "balance": profile.balance
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )