from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from feed.models import Profile

# Sign Up Form - extend Django UserCreation form to expose only
# username, password1 and password2
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "pfp"]
