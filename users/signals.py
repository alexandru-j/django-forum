from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from users.profiles.models import UserProfile
from .models import User

__all__ = ["create_user_profile", "delete_user_profile"]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            try:
                UserProfile.objects.create(
                    user=instance,
                    display_name=instance.username
                )
            except Exception as e:
                print(f"Something went wrong while creating the user profile: {e}")


@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    with transaction.atomic():
        try:
            UserProfile.objects.get(user=instance).delete()
        except Exception as e:
            print(f"Something went wrong while deleting the user profile: {e}")
