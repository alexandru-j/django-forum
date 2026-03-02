from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, resolve_url
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Notification


__all__ = ["NotificationListView", "NotificationDeleteView", "NotificationReadView"]


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/list.html"
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class NotificationDeleteView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Notification
    template_name = "notifications/_delete_form.html"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get("pk"), user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(resolve_url("notification-list"))


class NotificationReadView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Notification
    template_name = "notifications/_read_form.html"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get("pk"), user=self.request.user, read=False)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_as_read()
        return HttpResponseRedirect(resolve_url("notification-list"))
