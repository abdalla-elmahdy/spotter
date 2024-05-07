from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from util.mixins import OwnerRequiredMixin
from .forms import SessionForm, WorkoutForm
from .models import Session, Workout

CustomUser = get_user_model()

class SessionListView(LoginRequiredMixin, generic.ListView):
    """
    Get:
        Displays a list of the logged-in user's created sessions
    Context:
        - session_list: iterable of the logged-in user's created sessions
    Template name: plans/list.html
    """

    context_object_name = "session_list"
    template_name = "plans/list.html"

    def get_queryset(self):
        return CustomUser.objects.get(id=self.request.user.id).sessions.all()


class DashboardView(LoginRequiredMixin ,generic.DetailView):
    """
    Get:
        Displays details of the upcoming session
    Context:
        - session: an instance of Session model
    Template used: plans/dashboard.html

    """

    model = Session
    context_object_name = "session"
    
    template_name = "plans/dashboard.html"

    def get_object(self, queryset=None):
        queryset = CustomUser.objects.get(id=self.request.user.id).sessions.all()
        obj = queryset.first()
        return obj


class SessionCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Get:
        Displays an instance of Session form
    Post:
        Creates a new instance of Session and set its user to current logged in user
    Context:
        - form: an instance of SessionForm form
    Template used: plans/create.html
    """

    model = Session
    form_class = SessionForm
    template_name = "plans/create.html"

    def get_success_url(self):
        return reverse("plans:detail", args=[str(self.object.id)])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SessionDetailView(OwnerRequiredMixin, generic.DetailView):
    """
    Get:
        Displays details of an individual session instance
    Context:
        - session: an instance of Session model
    Template used: plans/detail.html

    """

    model = Session
    context_object_name = "session"
    template_name = "plans/detail.html"

class SessionDeleteView(OwnerRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    """
    Uses the instance's pk passed in the url path to retrieve it from DB
    Get:
        Displays a confirmation form to delete the instance or cancel
    Post:
        Deletes the instance if the current user as owner, otherwise returns 403 response
    """

    model = Session
    context_object_name = "session"
    template_name = "plans/delete.html"
    success_url = reverse_lazy("plans:dashboard")


class WorkoutCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Get:
        Displays an instance of Workout form
    Post:
        Creates a new instance of Project and set its owner to current logged in user
    Context:
        - form: an instance of ProjectForm form
    Template used: plans/workout_create.html
    """

    model = Workout
    form_class = WorkoutForm
    template_name = "plans/workout_create.html"

    def get_success_url(self):
        return reverse("plans:detail", args=[str(self.kwargs["session"])])

    def form_valid(self, form):
        form.instance.user = self.request.user
        session = get_object_or_404(Session, pk=self.kwargs["session"])
        form.instance.session = session
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_session"] = self.kwargs["session"]
        return context


class WorkoutUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Uses the instance's pk passed in the url path to retrieve it from DB
    Get:
        Displays an instance WorkoutForm model populated with the instance's data
    Post:
        Updates an instance of Workout model using WorkoutForm that has the current user as owner,
        otherwise returns 403 response
    Context:
        - Workout: the instance of Workout the user wants to update
        - form: an instance of WorkoutForm
    Template used: plans/workout_update.html
    """

    model = Workout
    form_class = WorkoutForm
    template_name = "plans/workout_update.html"
    context_object_name = "workout"

    def get_success_url(self):
        return reverse("plans:dashboard")

class WorkoutDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Uses the instance's pk passed in the url path to retrieve it from DB
    Get:
        Displays a confirmation form to delete the instance or cancel
    Post:
        Deletes the instance if the current user as owner, otherwise returns 403 response
    """

    model = Workout
    context_object_name = "workout"
    template_name = "plans/workout_delete.html"
    success_url = reverse_lazy("plans:dashboard")