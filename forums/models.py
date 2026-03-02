from django.db import models
from django.urls import reverse

__all__ = ["Forum"]


class Forum(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=255, blank=True)
    
    post_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Forum(nume={self.name})"

    def get_absolute_url(self) -> str:
        return reverse("forum-detail", kwargs={"pk": self.pk})
