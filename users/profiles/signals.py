from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from activity.models import Activity
from users.notifications.models import Notification
from .models import ProfileComment

__all__ = ["on_create_comment"]


@receiver(post_save, sender=ProfileComment)
def on_create_comment(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            author=instance.author
        )

        if instance.author != instance.profile.user:
            Notification.objects.create(
                tag="info",
                message=f'<a href="{instance.author.get_absolute_url()}">{instance.author}</a> a adaugat un comentariu <a href="{instance.profile.get_absolute_url()}">profilului tau</a>!',
                user=instance.profile.user
            )

@receiver(pre_delete, sender=ProfileComment)
def on_delete_comment(sender, instance, created, **kwargs):
    Activity.objects.get(object_id=instance.pk).delete()
