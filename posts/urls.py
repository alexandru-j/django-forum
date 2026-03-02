from django.urls import path

from .views import (
    PostDetailView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("forums/<int:forum_id>/new/", PostCreateView.as_view(), name="post-create"),
]
