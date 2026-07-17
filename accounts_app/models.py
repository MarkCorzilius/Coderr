from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Type(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        BUSINESS = 'business', 'Business'

    type = models.CharField(choices=Type.choices, default=Type.CUSTOMER, max_length=20)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)