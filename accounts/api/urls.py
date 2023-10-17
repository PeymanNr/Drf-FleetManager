from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.api.views import UserRegisterAPIView
from company.api.views import SendOTPView, VerifyOTPView

urlpatterns = [
    path('user/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('user/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('user/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

]
