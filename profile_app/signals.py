from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts_app.models import User
from profile_app.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)