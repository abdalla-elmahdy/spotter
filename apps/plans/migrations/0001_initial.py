# Generated by Django 4.2.3 on 2024-05-07 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("desc", models.TextField()),
                ("starting_prompt", models.CharField(max_length=100)),
                ("right_wrist", models.IntegerField(blank=True, null=True)),
                ("left_wrist", models.IntegerField(blank=True, null=True)),
                ("right_elbow", models.IntegerField(blank=True, null=True)),
                ("left_elbow", models.IntegerField(blank=True, null=True)),
                ("right_shoulder", models.IntegerField(blank=True, null=True)),
                ("left_shoulder", models.IntegerField(blank=True, null=True)),
                ("right_hip", models.IntegerField(blank=True, null=True)),
                ("left_hip", models.IntegerField(blank=True, null=True)),
                ("right_knee", models.IntegerField(blank=True, null=True)),
                ("left_knee", models.IntegerField(blank=True, null=True)),
                ("right_ankle", models.IntegerField(blank=True, null=True)),
                ("left_ankle", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.DateTimeField()),
                ("workouts_break", models.IntegerField()),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("UP", "Upcoming"),
                            ("UF", "Unfinished"),
                            ("FN", "Finished"),
                        ],
                        default="UP",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "ordering": ["-time"],
            },
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sets", models.IntegerField()),
                ("reps_per_set", models.IntegerField()),
                ("break_time", models.IntegerField()),
                (
                    "Exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workouts",
                        to="plans.exercise",
                    ),
                ),
                (
                    "Session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workouts",
                        to="plans.session",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="session",
            index=models.Index(fields=["-time"], name="plans_sessi_time_f5c0b2_idx"),
        ),
    ]
