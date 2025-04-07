from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.UserRegistrationView.as_view()),
    path('reset-password-request/', views.RequestPasswordResetView.as_view(), name='password_reset_request'),
    path('reset-password/<slug:token>/', views.PasswordResetView.as_view(), name='password_reset'),
]

