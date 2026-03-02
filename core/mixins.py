from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


__all__ = ["IsAuthorMixin"]


class IsAuthorMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if self.object.author != self.request.user:
            return HttpResponseForbidden()

        return response
        
