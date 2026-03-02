from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from activity.models import Activity
from users.notifications.models import Notification
from .models import Comment

__all__ = ["on_create_comment", "on_delete_comment"]


@receiver(post_save, sender=Comment)
def on_create_comment(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            try:
                instance.post.comment_count += 1
                instance.post.save()
                instance.author.profile.comment_count += 1
                instance.author.profile.save()
            except Exception as e:
                print(f"Something went wrong while updating the comment count: {e}")

        Activity.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            author=instance.author
        )

        if instance.author != instance.post.author:
            Notification.objects.create(
                tag="info",
                message=f'<a href="{instance.author.get_absolute_url()}">{instance.author}</a> a adaugat un comentariu postarii tale <a href="{instance.post.get_absolute_url()}">{instance.post.title}</a> din <a href="{instance.post.forum.get_absolute_url()}">{instance.post.forum.name}</a>!',
                user=instance.post.author
            )


@receiver(pre_delete, sender=Comment)
def on_delete_comment(sender, instance, **kwargs):
    with transaction.atomic():
        try:
            instance.post.comment_count -= 1
            instance.post.save()
            instance.author.profile.comment_count -= 1
            instance.author.profile.save()
        except Exception as e:
            print(f"Something went wrong while updating the post count: {e}")

    Activity.objects.get(content_type=ContentType.objects.get_for_model(instance),object_id=instance.pk).delete()
