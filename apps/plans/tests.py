from django.test import TestCase
from django.urls import reverse
from .models import Session, Exercise, Workout, MinAngles, MaxAngles
from django.utils import timezone

class SessionModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='test_user', email='test@example.com', password='test_password')
        self.session = Session.objects.create(user=self.user, time=timezone.now(), workouts_break=5)

    def test_get_absolute_url(self):
        expected_url = reverse('plans:detail', args=[self.session.id])
        self.assertEqual(self.session.get_absolute_url(), expected_url)

class ExerciseModelTest(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(name='Push-up', desc='Description', starting_prompt='Start')

    def test_str_representation(self):
        self.assertEqual(str(self.exercise), 'Push-up')

class WorkoutModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='test_user', email='test@example.com', password='test_password')
        self.session = Session.objects.create(user=self.user, time=timezone.now(), workouts_break=5)
        self.exercise = Exercise.objects.create(name='Push-up', desc='Description', starting_prompt='Start')
        self.workout = Workout.objects.create(session=self.session, exercise=self.exercise, sets=3, reps_per_set=10, break_time=60)

    def test_workout_creation(self):
        self.assertEqual(self.workout.session, self.session)
        self.assertEqual(self.workout.exercise, self.exercise)
        self.assertEqual(self.workout.sets, 3)
        self.assertEqual(self.workout.reps_per_set, 10)
        self.assertEqual(self.workout.break_time, 60)

class AngleModelTest(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(name='Push-up', desc='Description', starting_prompt='Start')
        self.min_angles = MinAngles.objects.create(exercise=self.exercise, right_wrist=90, left_wrist=90)
        self.max_angles = MaxAngles.objects.create(exercise=self.exercise, right_wrist=180, left_wrist=180)

    def test_angle_representation(self):
        self.assertEqual(str(self.min_angles), 'Push-up')
        self.assertEqual(str(self.max_angles), 'Push-up')

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Session, Workout
from .forms import SessionForm, WorkoutForm

CustomUser = get_user_model()

class ViewsIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.session = Session.objects.create(user=self.user, time='2024-01-01 12:00:00', workouts_break=5)
        self.workout = Workout.objects.create(session=self.session, exercise='Push-up', sets=3, reps_per_set=10, break_time=60)

    def test_session_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/list.html')
    
    def test_dashboard_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/dashboard.html')

    def test_session_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/create.html')

    def test_session_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_detail', kwargs={'pk': self.session.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/detail.html')

    def test_session_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_delete', kwargs={'pk': self.session.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/delete.html')

    def test_workout_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:workout_create', kwargs={'session': self.session.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/workout_create.html')

    def test_workout_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:workout_update', kwargs={'pk': self.workout.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/workout_update.html')

    def test_workout_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:workout_delete', kwargs={'pk': self.workout.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/workout_delete.html')

    def test_session_api_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_api'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions for API response validation

    def test_session_manager_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('plans:session_manager', kwargs={'pk': self.session.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/session_manager.html')