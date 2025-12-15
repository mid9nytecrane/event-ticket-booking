from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
        
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(
        max_length=10,
        blank=True,

    )

    town = models.CharField(
        max_length=100,
        blank=True,

    )

    def __str__(self) -> str:
        return f"{self.user}'s profile"

