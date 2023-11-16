from rest_framework import serializers
from django_filters import rest_framework as filters
from tracking.metrics import is_inside_tehran, get_filtered_speed_records, get_filtered_acceleration_records, \
    calculate_distance, calculate_distance_outside_tehran
from tracking.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CarInformationSerializer(serializers.ModelSerializer):
    is_tehran = serializers.SerializerMethodField()
    is_speed_high = serializers.SerializerMethodField()
    is_acceleration_high = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ('car_id', 'is_tehran', 'is_speed_high', 'is_acceleration_high', 'latitude', 'longitude', 'created_at')

    def get_is_tehran(self, obj):
        return is_inside_tehran(obj.latitude, obj.longitude)

    def get_is_speed_high(self, obj):
        if obj.speed >= 120:
            return True
        return False

    def get_is_acceleration_high(self, obj):
        if obj.acceleration >= 30:
            return True
        return False


class ReportFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Location
        fields = ['start_date', 'end_date']


class ReportSerializer(serializers.ModelSerializer):
    calculate_distance = serializers.SerializerMethodField()
    distance_dangerous_acceleration = serializers.SerializerMethodField()
    distance_dangerous_speed = serializers.SerializerMethodField()
    calculate_distance_outside_tehran = serializers.SerializerMethodField()
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)

    class Meta:
        model = Location
        fields = [
            'start_date', 'end_date', 'car_id', 'distance_dangerous_speed',
            'distance_dangerous_acceleration', 'calculate_distance_outside_tehran', 'calculate_distance'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        ret['start_date'] = request.query_params.get('start_date', None)
        ret['end_date'] = request.query_params.get('end_date', None)
        return ret

    def get_distance_dangerous_speed(self, obj):
        car_id = obj.car_id
        start_date = self.context.get('request').query_params.get('start_date', None)
        end_date = self.context.get('request').query_params.get('end_date', None)

        if start_date is not None and end_date is not None:
            distance = get_filtered_speed_records(car_id, start_date, end_date)
            return distance if distance is not None else 0  # Replace 0 with a default value if needed
        else:
            return 0

    def get_distance_dangerous_acceleration(self, obj):
        car_id = obj.car_id
        start_date = self.context.get('request').query_params.get('start_date', None)
        end_date = self.context.get('request').query_params.get('end_date', None)
        distance_acceleration = get_filtered_acceleration_records(car_id, start_date, end_date)

        return distance_acceleration

    def get_calculate_distance_outside_tehran(self, obj):
        car_id = obj.car_id
        start_date = self.context.get('request').query_params.get('start_date', None)
        end_date = self.context.get('request').query_params.get('end_date', None)
        distance_outside_tehran = calculate_distance_outside_tehran(car_id, start_date, end_date)

        return distance_outside_tehran

    def get_calculate_distance(self, obj):
        car_id = obj.car_id
        start_date = self.context.get('request').query_params.get('start_date', None)
        end_date = self.context.get('request').query_params.get('end_date', None)
        calculate = calculate_distance(car_id, start_date, end_date)

        return calculate
