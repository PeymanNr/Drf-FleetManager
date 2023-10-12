from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.views import UserRegisterAPIView

urlpatterns = [
    path('user/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user-login'),
]
