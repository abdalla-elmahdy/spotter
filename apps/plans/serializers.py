from rest_framework import serializers
from .models import Session, Workout, Exercise, MinAngles, MaxAngles




class MinAnglesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinAngles
        fields = (
            "right_wrist",
            "left_wrist",
            "right_elbow",
            "left_elbow",
            "right_shoulder",
            "left_shoulder",
            "right_hip",
            "left_hip",
            "right_knee",
            "left_knee",
            "right_ankle",
            "left_ankle",
        )

class MaxAnglesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaxAngles
        fields = (
            "right_wrist",
            "left_wrist",
            "right_elbow",
            "left_elbow",
            "right_shoulder",
            "left_shoulder",
            "right_hip",
            "left_hip",
            "right_knee",
            "left_knee",
            "right_ankle",
            "left_ankle",
        )

class ExerciseSerializer(serializers.ModelSerializer):
    min = MinAnglesSerializer(read_only=True, many=True)
    max = MaxAnglesSerializer(read_only=True, many=True)
    class Meta:
        model = Exercise
        fields = (
            "name",
            "desc",
            "starting_prompt",
            "min",
            "max"
        )

class WorkoutSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="exercise.name")
    desc = serializers.ReadOnlyField(source="exercise.desc")
    starting_prompt = serializers.ReadOnlyField(source="exercise.starting_prompt")
    exercise = ExerciseSerializer(read_only=True)
    # min = MinAnglesSerializer()
    # max = MaxAnglesSerializer()
    # right_wrist = serializers.ReadOnlyField(source="exercise.right_wrist")
    # left_wrist = serializers.ReadOnlyField(source="exercise.left_wrist")
    # right_elbow = serializers.ReadOnlyField(source="exercise.right_elbow")
    # left_elbow =serializers.ReadOnlyField(source="exercise.left_elbow")
    # right_shoulder = serializers.ReadOnlyField(source="exercise.right_shoulder")
    # left_shoulder =serializers.ReadOnlyField(source="exercise.left_shoulder")
    # right_hip = serializers.ReadOnlyField(source="exercise.right_hip")
    # left_hip = serializers.ReadOnlyField(source="exercise.left_hip")
    # right_knee = serializers.ReadOnlyField(source="exercise.right_knee")
    # left_knee = serializers.ReadOnlyField(source="exercise.left_knee")
    # right_ankle = serializers.ReadOnlyField(source="exercise.right_ankle")
    # left_ankle = serializers.ReadOnlyField(source="exercise.left_ankle")
    class Meta:
        model = Workout
        fields = (
            "name",
            "sets",
            "reps_per_set", 
            "break_time",
            "desc",
            "starting_prompt",
            "exercise",
            )


class SessionSerializer(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True)
    class Meta:
        model = Session
        fields = ("workouts_break", "workouts", "state")

