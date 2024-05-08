from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = "pages/home.html"

class SessionManagerView(LoginRequiredMixin, TemplateView):
    template_name = "pages/session_manager.html"