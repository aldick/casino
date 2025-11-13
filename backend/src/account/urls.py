from django.urls import path

from . import views


urlpatterns = [
    path("jwt/login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path("jwt/refresh/", views.CustomTokenRefreshView.as_view(), name="jwt-refresh"),
	path("logout/", views.LogoutView.as_view(), name="logout"),
]