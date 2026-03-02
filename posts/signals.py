from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from activity.models import Activity
from .models import Post

__all__ = ["on_create_post", "on_delete_post"]


@receiver(post_save, sender=Post)
def on_create_post(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            try:
                instance.forum.post_count += 1
                instance.forum.save()
                instance.author.profile.post_count += 1
                instance.author.profile.save()
            except Exception as e:
                print(f"Something went wrong while updating the post count: {e}")

        Activity.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            author=instance.author
        )


@receiver(pre_delete, sender=Post)
def on_delete_post(sender, instance, **kwargs):
    with transaction.atomic():
        try:
            instance.forum.post_count -= 1
            instance.forum.save()
            instance.author.profile.post_count -= 1
            instance.author.profile.save()
        except Exception as e:
            print(f"Something went wrong while updating the post count: {e}")

    Activity.objects.get(object_id=instance.pk).delete()
