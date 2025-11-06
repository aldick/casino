from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import DepositSerializer
from .models import DepositHistory


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        
        refresh_token = data.get("refresh")
        if refresh_token is None:
            raise AuthenticationFailed("Unauthenticated")
            
        jwt_settings = settings.SIMPLE_JWT

        response.set_cookie(
            key=jwt_settings.get("AUTH_COOKIE_REFRESH", "refresh"),
            value=refresh_token,
            httponly=jwt_settings.get("AUTH_COOKIE_HTTP_ONLY", True),
            secure=jwt_settings.get("AUTH_COOKIE_SECURE", False),
            samesite=jwt_settings.get("AUTH_COOKIE_SAMESITE", "Lax"),
        )
        
        return response
    
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        jwt_settings = settings.SIMPLE_JWT

        refresh_cookie_name = jwt_settings.get("AUTH_COOKIE_REFRESH", "refresh")
        refresh_token = request.COOKIES.get(refresh_cookie_name)
        if not refresh_token:
            return Response({"error": "No refresh token cookie"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        data = response.data

        if jwt_settings.get("ROTATE_REFRESH_TOKENS", False) and "refresh" in data:
            response.set_cookie(
                key=jwt_settings.get("AUTH_COOKIE_REFRESH", "refresh"),
                value=data["refresh"],
                httponly=jwt_settings.get("AUTH_COOKIE_HTTP_ONLY", True),
                secure=jwt_settings.get("AUTH_COOKIE_SECURE", True),
                samesite=jwt_settings.get("AUTH_COOKIE_SAMESITE", "Lax"),
            )

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"},
                            status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        return response
    

class DepositView(APIView):
    def get(self, request):
        return Response({
            "balance": request.user.balance
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        
        if serializer.is_valid():
            deposit = serializer.validated_data["deposit"]
            user = request.user
            
            deposit_history = DepositHistory(
                user=user,
                value=deposit
            )
            deposit_history.save()
            
            user.balance += deposit
            user.save()
            
            return Response(
                {
                    "balance": "Successful replenishment of the balance",
                    "deposit": deposit,
                    "balance": user.balance
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )