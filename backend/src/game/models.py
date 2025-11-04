from django.db import models
from django.conf import settings


class Game(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='games'
	)
    bet = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
    )
    payout = models.PositiveIntegerField()
    result = models.CharField(max_length=100)
    
    @property
    def is_win(self):
        return True if self.payout != 0 else False
    
    def __str__(self):
        return f"Game #{self.id} - {self.name} ({self.user})"
 