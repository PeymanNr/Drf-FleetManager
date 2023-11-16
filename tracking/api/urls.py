from django.urls import path
from tracking.api.views import LocationAPIView, CarInformationView, \
    ReportAPIView

urlpatterns = [
    path('location/', LocationAPIView.as_view(), name='location'),
    path('car-information/<int:car_id>/', CarInformationView.as_view(),
         name='car_information'),
    path('reports/<int:car_id>/', ReportAPIView.as_view(), name='report-api'),

]
