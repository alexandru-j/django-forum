from django.urls import path

from .views import ForumDetailView, ForumListView


urlpatterns = [
    path("", ForumListView.as_view(), name="forum-list"),
    path("forums/<int:pk>/", ForumDetailView.as_view(), name="forum-detail"),
]
