from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class CustomUser(AbstractUser):
    GENDER = {
        "male":"MALE",
        "female":"FEMALE",
    }

    gender = models.CharField(max_length=10, choices=GENDER, default="")
    location = models.CharField(max_length=255)
