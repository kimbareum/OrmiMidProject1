from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'nickname']
        # fields = UserCreationForm.Meta.fields + ('email',)


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileUpdateForm(forms.ModelForm):

    nickname = forms.CharField(max_length=15)

    class Meta:
        model = Profile
        fields = ['image', 'state', 'nickname']