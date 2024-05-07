from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm

class CustomUserCreationForm(SignupForm):
    class Meta:
        model = get_user_model()
        fields = (
        "email",
        "first_name",
        "last_name",
        "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
        "email",
        "first_name",
        "last_name",
        "username",
        )