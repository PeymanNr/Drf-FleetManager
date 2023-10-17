from django.urls import path
from .views import CreateCompanyView

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='send-otp'),
]