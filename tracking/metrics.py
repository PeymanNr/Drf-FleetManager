from .api.utils import calculate_distance_points
from .models import Location
from datetime import timedelta


def is_inside_tehran(latitude, longitude):
    # cache_key = f'is_inside_tehran_{latitude}_{longitude}'
    # result = cache.get(cache_key)
    # if result is not None:
    #     return result

    tehran_boundary = {
        'latitude_min': 35.5,
        'latitude_max': 35.9,
        'longitude_min': 51.1,
        'longitude_max': 51.7
    }

    if (tehran_boundary['latitude_min'] <= latitude <= tehran_boundary['latitude_max'] and
            tehran_boundary['longitude_min'] <= longitude <= tehran_boundary['longitude_max']):
        return 'It is inside Tehran'
    else:
        return 'It is not inside Tehran'


def get_filtered_acceleration_records(car_id, start_date, end_date):
    filtered_locations = Location.objects.filter(
        car_id=car_id,
        created_at__gte=start_date,
        created_at__lt=end_date,
        acceleration__range=(40, 60)
    ).order_by('created_at')

    total_duration = timedelta()
    distance = 0
    prev_location = None

    for location in filtered_locations:
        if prev_location:
            distance += calculate_distance_points(
                prev_location.latitude, prev_location.longitude, location.latitude, location.longitude
            )
            duration = location.created_at - prev_location.created_at
            total_duration += duration
        prev_location = location

    return distance, total_duration.total_seconds()


def get_filtered_speed_records(car_id, start_date, end_date):
    locations = Location.objects.filter(
        car_id=car_id,
        created_at__gte=start_date,
        created_at__lt=end_date,
        speed__gte=120
    ).order_by('created_at')

    total_distance = 0
    total_duration = timedelta()

    for i in range(len(locations) - 1):
        start_location = locations[i]
        end_location = locations[i + 1]

        total_distance += calculate_distance_points(
            start_location.latitude, start_location.longitude, end_location.latitude, end_location.longitude
        )

        duration = end_location.created_at - start_location.created_at

        total_duration += duration

    return total_distance, total_duration.total_seconds()


def calculate_distance_outside_tehran(car_id, start_date, end_date):
    filtered_locations = Location.objects.filter(
        car_id=car_id,
        created_at__gte=start_date,
        created_at__lt=end_date
    ).order_by('created_at')

    total_distance = 0
    prev_location = None
    total_duration = timedelta()

    for location in filtered_locations:
        if prev_location and not is_inside_tehran(location.latitude, location.longitude):
            distance = calculate_distance_points(
                prev_location.latitude, prev_location.longitude, location.latitude, location.longitude
            )
            duration = location.created_at - prev_location.created_at
            total_distance += distance
            total_duration += duration

        prev_location = location

    return total_distance, total_duration.total_seconds()


def calculate_distance(car_id, start_date, end_date):
    locations_distance = Location.objects.filter(
        car_id=car_id,
        created_at__gte=start_date,
        created_at__lt=end_date
    ).order_by('created_at')
    total_duration = timedelta()
    distance = 0
    prev_location = None

    for location in locations_distance:
        if prev_location:
            distance += calculate_distance_points(
                prev_location.latitude, prev_location.longitude, location.latitude, location.longitude
            )
            duration = location.created_at - prev_location.created_at
            total_duration += duration
        prev_location = location

    return distance, total_duration.total_seconds()
