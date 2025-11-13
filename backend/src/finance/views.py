from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DepositHistory, Promocode, UsedPromocode
from .serializers import DepositSerializer


def calculate_payout(deposit: Decimal, promocode: Promocode | None) -> Decimal:
    """
    Returns final payout (deposit + bonus) based on promocode type.
    """
    
    if promocode is None:
        return deposit

    if not promocode.is_valid():
        raise ValueError("Promocode is not active or expired")

    discount_value = Decimal(promocode.discount_value)

    if promocode.discount_type == Promocode.DiscountType.FIXED:
        payout = deposit + discount_value
    else:
        payout = deposit * (1 + discount_value / 100)

    return payout.quantize(Decimal("0.01"))


class DepositView(APIView):
    def get(self, request):
        return Response({"balance": request.user.balance}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        deposit = Decimal(serializer.validated_data["deposit"])
        promocode_name = request.query_params.get("promocode", None)

        promocode = (
            Promocode.objects.filter(name=promocode_name, is_active=True).first()
            if promocode_name
            else None
        )
        
        
        if promocode is None and promocode_name is not None:
            return Response({
                "promocode": "Promocode is not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if promocode:
            if UsedPromocode.objects.filter(user=user, promocode=promocode).exists():
                return Response(
                    {"promocode": "You have already used this promocode."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not promocode.is_valid():
                return Response(
                    {"promocode": "Promocode is not active or expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            payout = calculate_payout(deposit, promocode)
        except ValueError as e:
            return Response({"promocode": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        deposit_history = DepositHistory.objects.create(user=user, value=deposit)

        if promocode:
            UsedPromocode.objects.create(user=user, promocode=promocode, deposit=deposit_history)

        user.balance += payout
        user.save(update_fields=["balance"])

        return Response(
            {
                "message": "Successful balance replenishment",
                "deposit": float(deposit),
                "promocode": promocode_name,
                "bonus": float(payout - deposit),
                "balance": float(user.balance),
            },
            status=status.HTTP_200_OK,
        )
