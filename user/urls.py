from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.Registration.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name="profile"),
    path('profile/update', views.ProfileUpdate.as_view(), name="pf-update"),
]