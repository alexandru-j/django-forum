from django.urls import path

from .views import NotificationListView, NotificationReadView, NotificationDeleteView


urlpatterns = [
    path("account/notifications/", NotificationListView.as_view(), name="notification-list"),
    path("account/notifications/<pk>/read/", NotificationReadView.as_view(), name="notification-read"),
    path("account/notifications/<pk>/delete/", NotificationDeleteView.as_view(), name="notification-delete"),
]
