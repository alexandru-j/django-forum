from django.urls import path

from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path("posts/<int:post_id>/reply/", CommentCreateView.as_view(), name="comment-create"),    
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),    
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),    
]
