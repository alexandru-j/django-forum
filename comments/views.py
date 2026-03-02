from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView

from core.mixins import IsAuthorMixin
from posts.models import Post
from .models import Comment

__all__ = ["CommentCreateView", "CommentUpdateView", "CommentDeleteView"]


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["message"]
    template_name = "comments/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.post_id = get_object_or_404(Post, pk=self.kwargs.get("post_id")).pk
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["post_id"] = self.post_id
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_id = self.post_id
        self.object.author_id = self.request.user.pk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CommentUpdateView(IsAuthorMixin, UpdateView):
    model = Comment
    fields = ["message"]
    template_name = "comments/update.html"


class CommentDeleteView(IsAuthorMixin, DeleteView):
    model = Comment
    template_name = "comments/delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()
