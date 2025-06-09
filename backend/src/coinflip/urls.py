from django.urls import path

from .views import CoinFlipView


urlpatterns = [
	path("", CoinFlipView.as_view(), name="coin-flip"),
]