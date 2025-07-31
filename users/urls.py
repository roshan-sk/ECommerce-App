from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('admin-register/', AdminRegisterView.as_view(), name='admin-register'),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('all/', GetAllUsersView.as_view(), name='get-all-users'),
]
