from django.forms import ModelForm, widgets

from .models import Session, Workout


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = (
            "time",
            "workouts_break",
        )
        widgets = {
            "time": widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        help_texts = {
            "workouts_break": "(in seconds)"
        }

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = (
            "exercise",
            "sets",
            "reps_per_set",
            "break_time",
        )
        
        help_texts = {
            "break_time": " Time between sets (in seconds)"
        }

