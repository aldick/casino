from django.urls import path

from .views import PlinkoView


urlpatterns = [
	path('', PlinkoView.as_view(), name="plinko"),
]