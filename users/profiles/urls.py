from django.urls import path

from .views import (
    UserProfileUpdateView,
    UserProfileDetailView,
    UserProfileListView,
    ProfileCommentCreateView,
    ProfileCommentUpdateView,
    ProfileCommentDeleteView
)

urlpatterns = [
    path("account/profile/", UserProfileUpdateView.as_view(), name="profile-update"),
    path("profiles/", UserProfileListView.as_view(), name="profile-list"),
    path("profiles/<int:pk>/", UserProfileDetailView.as_view(), name="profile-detail"),
    path("profiles<int:profile_id>/reply/", ProfileCommentCreateView.as_view(), name="profilecomment-create"),    
    path("profilecomments/<int:pk>/update/", ProfileCommentUpdateView.as_view(), name="profilecomment-update"),    
    path("profilecomments/<int:pk>/delete/", ProfileCommentDeleteView.as_view(), name="profilecomment-delete"),    
]
