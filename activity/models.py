from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

__all__ = ["Activity"]


class Activity(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ["-created_at"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"Activity(content_type={self.content_type}, object_id={self.object_id} author={self.author})"
