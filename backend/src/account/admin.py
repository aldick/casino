from django.contrib import admin

from .models import User, DepositHistory


@admin.register(User)
class User(admin.ModelAdmin):
    pass

@admin.register(DepositHistory)
class DepositHistory(admin.ModelAdmin):
    pass
