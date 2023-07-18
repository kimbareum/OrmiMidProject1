from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from .models import Profile
from .forms import RegisterForm, LoginForm


User = get_user_model()


def get_banner(main="Our Blog", sub="Python, Django, JavaScript & Life", text=''):
    banner = {
        "main": main,
        "sub": sub,
        "text": text,
    }
    return banner


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


# ### Profile


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
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
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.image = request.POST.get('image')
        profile.state = request.POST.get('state')
        profile.save()
        return redirect('user:profile')



# class ProfileWrite(APIView):

#     def post(self, request):
#         user = request.user # request.data.get('user')
#         print(request.data.get('user'))
#         image = request.data.get('image')
#         age = request.data.get('age')
#         try:
#             profile = Profile.objects.create(user=user, image=image, age=age)
#         except IntegrityError as e: 
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = ProfileSerializer(profile)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProfileUpdate(APIView):

#     def get(self, request):
#         user = request.user
#         try:
#             profile = Profile.objects.get(user=user)
#         except ObjectDoesNotExist as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         try:
#             profile = Profile.objects.get(user=user)
#         except ObjectDoesNotExist as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class ProfileDelete(APIView):

#     def post(self, request):
#         try:
#             profile = Profile.objects.get(user=request.user)
#         except ObjectDoesNotExist as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
#         profile.delete()
#         return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)