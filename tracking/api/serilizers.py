from rest_framework import serializers
from tracking.models import Location, Metric


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class MetricSerializer(serializers.Serializer):
    class Meta:
        model = Metric
        fields = '__all__'
