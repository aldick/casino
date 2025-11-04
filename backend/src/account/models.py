from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='profile'
	)
    
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
    )
    
    def __str__(self):
        return f"{self.user.username}: ${self.balance}"
    