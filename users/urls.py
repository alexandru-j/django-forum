from django.urls import path, include

from .views import AccountUpdateView, PasswordChangeView

urlpatterns = [
    path("account/", AccountUpdateView.as_view(), name="account-update"),
    path("account/change/password/", PasswordChangeView.as_view(), name="account-change-password"),
    path("", include("users.auth.urls")),    
    path("", include("users.notifications.urls")),    
    path("", include("users.profiles.urls")),    
]
