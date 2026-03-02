from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import IsAuthorMixin
from forums.models import Forum
from comments.models import Comment
from .models import Post

__all__ = [
    "PostDetailView",
    "PostListView",
    "PostCreateView",
    "PostUpdateView",
    "PostDeleteView",
]


class PostDetailView(ListView):
    model = Post
    template_name = "posts/detail.html"
    paginate_by = 5

    def get_queryset(self):
        self.post = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return Comment.objects.filter(post_id=self.post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.post
        return context


class PostListView(ListView):
    model = Post
    template_name = "posts/list.html"
    paginate_by = 20


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "posts/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, pk=self.kwargs.get("forum_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["forum"] = self.forum
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.forum_id = self.forum.pk
        self.object.author_id = self.request.user.pk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(IsAuthorMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "posts/update.html"


class PostDeleteView(IsAuthorMixin, DeleteView):
    model = Post
    template_name = "posts/delete.html"

    def get_success_url(self):
        return self.object.forum.get_absolute_url()
