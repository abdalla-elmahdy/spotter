from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    """
    Ensures that only the instance owner can take action.
    """

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)