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
        "workout/<int:pk>",
        views.WorkoutUpdateView.as_view(),
        name="workout_update",
    ),
    path(
        "workout/delete/<int:pk>/",
        views.WorkoutDeleteView.as_view(),
        name="workout_delete",
    ),
    path(
        "dashboard/",
        views.DashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "api/",
        views.SessionApiView.as_view(),
        name="session_api",
    ),
    path(
        "",
        views.SessionListView.as_view(),
        name="list",
    ),
]