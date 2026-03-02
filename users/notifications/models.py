from django.contrib.auth import get_user_model
from django.db import models

__all__ = ["Notifications"]


STATUS_CHOICES = {
    "info": "Information",
    "success": "Success",
    "warning": "Warning",
    "danger": "Error",
}


class Notification(models.Model):
    tag = models.CharField(choices=STATUS_CHOICES)
    message = models.TextField(max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification(tag={self.tag}, user={self.user})"

    def mark_as_read(self):
        self.read = True
        self.save()
