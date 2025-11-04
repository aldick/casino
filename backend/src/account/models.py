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
    