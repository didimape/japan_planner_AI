from math import radians, sin, cos, sqrt, atan2

def haversine(a, b):

    R = 6371  # km

    lat1, lon1 = a
    lat2, lon2 = b

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    h = (
        sin(dlat / 2) ** 2 +
        cos(radians(lat1)) *
        cos(radians(lat2)) *
        sin(dlon / 2) ** 2
    )

    return 2 * R * atan2(sqrt(h), sqrt(1 - h))


def estimate_time_minutes(distance_km, speed_kmh=4.5):

    return (distance_km / speed_kmh) * 60

def estimate_transport(distance_km):

    if distance_km < 1.5:

        minutes = (distance_km / 4.5) * 60

        return {
            "mode": "🚶 Andando",
            "minutes": int(minutes)
        }

    else:

        # Aproximación metro Tokio
        minutes = 10 + (distance_km / 30) * 60

        return {
            "mode": "🚇 Metro",
            "minutes": int(minutes)
        }