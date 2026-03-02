from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

__all__ = ["RegistrationForm"]


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email

