from django.urls import path

from .views import ActivityDetailView, ActivityListView

urlpatterns = [
    path("profiles/<int:pk>/activity/", ActivityDetailView.as_view(), name="activity-detail"),
    path("activity/", ActivityListView.as_view(), name="activity-list"),
]
