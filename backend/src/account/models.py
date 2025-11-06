from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
    )
    
    def __str__(self):
        return f"{self.username}: ${self.balance}"
    

class DepositHistory(models.Model):
    user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='deposit'
	)
    value = models.DecimalField(
        decimal_places=2,
        max_digits=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} has deposited ${self.value} at {self.created_at}"
    