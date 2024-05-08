from django.urls import path

from .views import HomePageView, SessionManagerView

app_name = "pages"

urlpatterns = [
    path("session-manager/", SessionManagerView.as_view(), name="session_manager"),
    path("", HomePageView.as_view(), name="home"),
]