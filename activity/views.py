from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from users.profiles.models import UserProfile
from .models import Activity

__all__ = ["ActivityDetailView"]


class ActivityDetailView(ListView):
    model = UserProfile
    template_name = "activity/detail.html"
    paginate_by = 8

    def get_queryset(self):
        self.profile = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return Activity.objects.filter(author_id=self.profile.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context


class ActivityListView(ListView):
    model = Activity
    template_name = "activity/list.html"
    paginate_by = 10
