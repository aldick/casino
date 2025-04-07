from django.urls import path
from . import views

urlpatterns = [
    path('flip/', views.CoinFlipView.as_view(), name='flip'),
]