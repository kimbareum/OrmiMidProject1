from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import check_password
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


class UserDeleteForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')