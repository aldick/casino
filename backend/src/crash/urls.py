from django.urls import path

from .views import CrashView


urlpatterns = [
	path('', CrashView.as_view(), name="crash"),
]