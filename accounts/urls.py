from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
