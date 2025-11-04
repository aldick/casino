from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('account.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    
    path("coin-flip/", include("coinflip.urls")),
    path("roulette/", include("roulette.urls")),
    path("crash/", include("crash.urls")),
    path("plinko/", include("plinko.urls"))
]
