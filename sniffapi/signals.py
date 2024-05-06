from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from sniffapi.models import ScentUser

@receiver(post_save, sender=User)
def create_scent_user(sender, instance, created, **kwargs):
    if created:
        ScentUser.objects.create(user=instance)