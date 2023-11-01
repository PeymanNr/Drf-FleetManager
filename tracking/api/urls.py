from django.urls import path
from tracking.api.views import LocationAPIView, MetricAPIView

urlpatterns = [
    path('location/', LocationAPIView.as_view(), name='location'),
    path('metric/', MetricAPIView.as_view(), name='metric'),

]
