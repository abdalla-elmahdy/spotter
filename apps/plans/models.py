from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()

class Session(models.Model):
    class StateChoices(models.TextChoices):
        UPCOMING = "UP", "Upcoming"
        UNFINISHED = "UF", "Unfinished"
        FINISHED = "FN", "Finished"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sessions")
    time = models.DateTimeField()
    workouts_break = models.IntegerField()
    state = models.CharField(max_length=2,
                             choices=StateChoices.choices,
                             default=StateChoices.UPCOMING)

    class Meta:
        ordering = ['time']
        indexes = [
            models.Index(fields=['time']),
        ]
    
    def get_absolute_url(self):
        return reverse("plans:detail", args=[str(self.id)])


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    starting_prompt = models.CharField(max_length=100)
    right_wrist = models.IntegerField(blank=True, null=True)
    left_wrist = models.IntegerField(blank=True, null=True)
    right_elbow = models.IntegerField(blank=True, null=True)
    left_elbow = models.IntegerField(blank=True, null=True)
    right_shoulder = models.IntegerField(blank=True, null=True)
    left_shoulder = models.IntegerField(blank=True, null=True)
    right_hip = models.IntegerField(blank=True, null=True)
    left_hip = models.IntegerField(blank=True, null=True)
    right_knee = models.IntegerField(blank=True, null=True)
    left_knee = models.IntegerField(blank=True, null=True)
    right_ankle = models.IntegerField(blank=True, null=True)
    left_ankle = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    session = models.ForeignKey(Session,
                                on_delete=models.CASCADE,
                                related_name="workouts")
    exercise = models.ForeignKey(Exercise,
                                 on_delete=models.CASCADE,
                                 related_name="workouts")
    sets = models.IntegerField()
    reps_per_set = models.IntegerField()
    break_time = models.IntegerField()



