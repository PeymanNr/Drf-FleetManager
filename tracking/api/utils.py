from django.core.cache import cache
import math


def calculate_distance_points(lat1, lon1, lat2, lon2):
    # Generate a unique key based on the function arguments
    cache_key = f"distance_{lat1}_{lon1}_{lat2}_{lon2}"

    # Check if the result is already in the cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    # If not in the cache, perform the calculation
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c

    # Cache the result for future use (expire in 1 hour, adjust as needed)
    cache.set(cache_key, distance, timeout=3600)

    return distance
