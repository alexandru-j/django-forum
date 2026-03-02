from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

__all__ = ["Comment"]


class Comment(models.Model):
    message = models.TextField(max_length=1200)
    
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment(author={self.author}, post={self.post.title} forum={self.post.forum.name})"

    def get_absolute_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.post.pk})
