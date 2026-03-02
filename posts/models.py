from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

__all__ = ["Post"]


class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=1200, blank=True)
    
    forum = models.ForeignKey("forums.Forum", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    comment_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Post(titlu={self.title}, author={self.author}, forum={self.forum.name})"

    def get_absolute_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.pk})
