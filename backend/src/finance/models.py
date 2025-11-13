from django.db import models
from django.utils import timezone
from django.conf import settings    
    
    
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


class Promocode(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE"
        FIXED = "FIXED"
    
    name = models.CharField(max_length=10,
                            unique=True)
    discount_type = models.CharField(choices=DiscountType.choices,
                                     default=DiscountType.FIXED)
    discount_value = models.DecimalField(max_digits=20, 
                                         decimal_places=2)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.name} ({self.discount_type}: {self.discount_value})"
    
    def is_valid(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date


class UsedPromocode(models.Model):
    user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='used_promocodes'
    )
    promocode = models.ForeignKey(
        Promocode,
        on_delete=models.PROTECT,
        related_name="used_by_users"
	)
    deposit = models.ForeignKey(
        DepositHistory,
        on_delete=models.CASCADE,
        related_name="users"
    )
    used_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = ("user", "promocode")
        ordering = ["-used_at"]
    
    def __str__(self):
        return f"{self.user.username} has used {self.promocode.name}"
    