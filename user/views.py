from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from myapp.utils.utils import get_banner

from .models import Profile
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, UserDeleteForm
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()


### Registration
class Registration(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm()
        context = {
            'title': '회원가입',
            'banner': get_banner(main='Join Us'),
            'form': form,
        }
        return render(request, 'user/user_register.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            return redirect('user:login')
        context = {
            'title': '회원가입',
            'banner': get_banner(main='Join Us'),
            'form': form,
        }
        return render(request, 'user/user_register.html', context)

### Login
class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()

        context = {
            'title': '로그인',
            'banner': get_banner(main='Login Blog'),
            'form': form,
        }
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('blog:list')
        context = {
            'title': '로그인',
            'banner': get_banner(main='Login Blog'),
            'form': form,
        }
        return render(request, 'user/user_login.html', context)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('blog:list')


class PasswordChange(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {
            'title': '패스워드 변경',
            'banner': get_banner(),
            'form': form,
        }
        return render(request, 'user/password_change.html', context)
    
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
        context = {
            'title': '패스워드 변경',
            'banner': get_banner(),
            'form': form,
            }
        return render(request, 'user/password_change.html', context)


class UserDelete(LoginRequiredMixin, View):

    def get(self, request):
        form = UserDeleteForm(request.user)
        context = {
            'title': '회원 탈퇴',
            'banner': get_banner(),
            'form': form,
            }
        return render(request, 'user/user_delete.html', context)
    
    def post(self, request):
        user = request.user
        form = UserDeleteForm(user, request.POST)
        if form.is_valid():
            user.is_active = False
            user.save()
            logout(request)
            return redirect('blog:list')
        
        context = {
            'title': '회원 탈퇴',
            'banner': get_banner(),
            'form': form,
            }
        return render(request, 'user/user_delete.html', context)


# ### Profile


class ProfileView(View):

    def get(self, request, user_id):
        try:
            profile = Profile.objects.select_related('user').get(user__pk=user_id)
        except ObjectDoesNotExist as e:
            messages.error(request, "해당 유저는 존재하지 않습니다.")
            return redirect('error')
        if not profile.user.is_active:
            messages.error(request, "해당 유저는 존재하지 않습니다.")
            return redirect('error')
        user = profile.user
        context = {
            "title": f"{user.nickname}의 프로필",
            'banner': get_banner(main=f"{user.username}'s Profile"),
            'profile': profile
        }
        return render(request, 'user/user_profile.html', context)


class ProfileUpdate(View):

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        context = {
            "title": f"{user.nickname}의 프로필",
            'banner': get_banner(main=f"{user.username}'s Profile"),
            'profile': profile
        }
        return render(request, 'user/profile_update.html', context)

    def post(self, request):
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.image = form.cleaned_data.get('image')
            profile.state = form.cleaned_data.get('state')
            profile.save()
            user.nickname = form.cleaned_data.get('nickname')
            user.save()
            return redirect('user:profile', user_id=user.pk)