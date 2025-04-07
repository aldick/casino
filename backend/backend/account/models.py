from django.db import models
from django.conf import settings


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	balance = models.IntegerField(default=0)

	def __str__(self):
		return f'Profile of {self.user.username}'

class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)