from django.db import models
from django.contrib.auth import get_user_model

__all__ = ["UserProfile", "ProfileComment"]


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=32)

    post_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"UserProfile(user={self.user.username}, post_count={self.post_count}, comment_count={self.comment_count})"

    def get_absolute_url(self) -> str:
        return self.user.get_absolute_url()


class ProfileComment(models.Model):
    message = models.TextField(max_length=1200)
    
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"ProfileComment(author={self.author}, profile={self.profile.user.username})"

    def get_absolute_url(self) -> str:
        return self.profile.get_absolute_url()
