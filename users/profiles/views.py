from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import IsAuthorMixin
from .models import UserProfile, ProfileComment

__all__ = [
    "UserProfileUpdateView",
    "UserProfileDetailView",
    "UserProfileListView",
    "ProfileCommentCreateView"
	"ProfileCommentUpdateView",
	"ProfileCommentDeleteView"
]


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ["display_name"]
    template_name = "profiles/_update_form.html"

    def get_object(self):
        return self.request.user.profile


class UserProfileDetailView(ListView):
    model = UserProfile
    template_name = "profiles/detail.html"
    paginate_by = 5

    def get_queryset(self):
        self.profile = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return ProfileComment.objects.filter(profile_id=self.profile.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        context["activities"] = self.profile.user.activity_set.select_related("content_type").all()[:3]
        return context


class UserProfileListView(ListView):
    model = UserProfile
    template_name = "profiles/list.html"
    paginate_by = 20


class ProfileCommentCreateView(LoginRequiredMixin, CreateView):
    model = ProfileComment
    fields = ["message"]
    template_name = "profiles/create_comment.html"

    def dispatch(self, request, *args, **kwargs):
        self.profile_id = get_object_or_404(UserProfile, pk=self.kwargs.get("profile_id")).pk
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["profile_id"] = self.profile_id
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile_id = self.profile_id
        self.object.author_id = self.request.user.pk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileCommentUpdateView(IsAuthorMixin, UpdateView):
    model = ProfileComment
    fields = ["message"]
    template_name = "profiles/update_comment.html"
    context_object_name = "comment"


class ProfileCommentDeleteView(IsAuthorMixin, DeleteView):
    model = ProfileComment
    template_name = "profiles/delete_comment.html"
    context_object_name = "comment"

    def get_success_url(self):
        return self.object.profile.get_absolute_url()
