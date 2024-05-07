from django.urls import path

from . import views

app_name = "plans"

urlpatterns = [
    path(
        "new/",
        views.SessionCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>",
        views.SessionDetailView.as_view(),
        name="detail",
    ),
    path(
        "delete/<int:pk>/",
        views.SessionDeleteView.as_view(),
        name="delete",
    ),
    path(
        "new-workout/<int:session>",
        views.WorkoutCreateView.as_view(),
        name="workout_create",
    ),
    path(
        "",
        views.DashboardView.as_view(),
        name="dashboard",
    ),
]