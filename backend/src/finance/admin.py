from django.contrib import admin

from .models import DepositHistory, Promocode, UsedPromocode


@admin.register(DepositHistory)
class DepositHistory(admin.ModelAdmin):
    pass

@admin.register(Promocode)
class Promocode(admin.ModelAdmin):
    pass

@admin.register(UsedPromocode)
class UsedPromocode(admin.ModelAdmin):
    pass
