from django.urls import path

from .views import RouletteView


urlpatterns = [
	path("", RouletteView.as_view(), name="roulette"),
]