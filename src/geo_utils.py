from math import radians, sin, cos, sqrt, atan2



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