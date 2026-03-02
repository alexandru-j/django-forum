from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from posts.models import Post
from .models import Forum

__all__ = ["ForumDetailView", "ForumListView"]


class ForumDetailView(ListView):
    model = Forum
    template_name = "forums/detail.html"
    paginate_by = 20

    def get_queryset(self):
        self.forum = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return Post.objects.filter(forum_id=self.forum.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.forum
        return context


class ForumListView(ListView):
    model = Forum
    template_name = "forums/list.html"
    context_object_name = "forums"
