from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'bet_display', 'payout_display', 'is_win')

    def bet_display(self, obj):
        return f"${obj.bet:,.2f}"
    bet_display.short_description = 'Bet'

    def payout_display(self, obj):
        return f"${obj.payout:,.2f}"
    payout_display.short_description = 'Payout'

    def is_win(self, obj):
        return obj.payout > 0
    is_win.boolean = True  
