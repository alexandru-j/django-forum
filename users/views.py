from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .models import User

__all__ = ["AccountUpdateView", "PasswordChangeView"]


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "accounts/update.html"
    success_url = reverse_lazy("account-update")

    def get_object(self):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, BasePasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("account-update")
