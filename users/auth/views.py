from django.conf import settings
from django.contrib.auth import (
    get_user_model,
    logout as auth_logout,
    login as auth_login
)
from django.contrib.auth.views import (
    RedirectURLMixin,
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.generic import FormView

from .forms import RegistrationForm

__all_ = ["LoginView", "LogoutView", "RegisterView"]


class LoginView(BaseLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class LogoutView(BaseLogoutView):
    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, "Te-ai deconectat cu success!")
        return super().post(request, *args, **kwargs)


class RegisterView(RedirectURLMixin, FormView):
    form_class = RegistrationForm
    template_name = "auth/register.html"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your REGISTER_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.REGISTER_REDIRECT_URL)

    def form_valid(self, form):
        user = get_user_model().objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
        )
        user.set_password(form.cleaned_data["password1"])
        user.save()
        auth_login(self.request, user) # Login dupa register
        messages.add_message(self.request, messages.SUCCESS, "Te-ai inregistrat cu success!")
        return super().form_valid(form)
