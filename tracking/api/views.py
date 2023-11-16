from django.http import Http404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from tracking.api.serializers import LocationSerializer, \
    CarInformationSerializer, ReportFilter, ReportSerializer
from tracking.models import Location
from django_filters.rest_framework import DjangoFilterBackend


class LocationAPIView(CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)


class CarInformationView(RetrieveAPIView):
    serializer_class = CarInformationSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        car_id = self.kwargs.get('car_id')
        try:
            queryset = Location.objects.filter(car_id=car_id).latest(
                'created_at')
        except Location.DoesNotExist:
            raise Http404("Location not found for the specified car_id.")
        return queryset


class ReportAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReportFilter
    serializer_class = ReportSerializer

    def get_queryset(self):
        car_id = self.kwargs.get('car_id')

        try:
            location = Location.objects.filter(car_id=car_id).order_by(
                'created_at').first()
            if not location:
                raise Location.DoesNotExist
        except Location.DoesNotExist:
            raise Http404("Location not found for the specified car_id.")

        return Location.objects.filter(pk=location.pk)
