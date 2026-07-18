from django.db import models
from accounts_app.models import User

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=75, default=' ')
    last_name = models.CharField(max_length=75, default=' ')
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    location = models.CharField(max_length=150, default='')
    tel = models.CharField(default=' ')
    description = models.TextField(max_length=300, default=' ')
    working_hours = models.CharField(default=' ', max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"