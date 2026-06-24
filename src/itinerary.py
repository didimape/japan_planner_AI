import numpy as np
from sklearn.cluster import KMeans

from math import radians, sin, cos, sqrt, atan2



def haversine(a, b):

    R = 6371

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


def sort_by_real_path(places):

    if not places:
        return []

    remaining = places.copy()

    ordered = [remaining.pop(0)]

    while remaining:

        last = ordered[-1]

        last_coords = (
            last["coordinates"]["lat"],
            last["coordinates"]["lng"]
        )

        next_place = min(
            remaining,
            key=lambda p: haversine(
                last_coords,
                (
                    p["coordinates"]["lat"],
                    p["coordinates"]["lng"]
                )
            )
        )

        ordered.append(next_place)
        remaining.remove(next_place)

    return ordered

def build_itinerary(
    ranked_places,
    days,
    hours_per_day=8
):

    # -------------------------
    # 1. SACAR SOLO LOS LUGARES
    # -------------------------

    places = [p for p, score in ranked_places]

    # -------------------------
    # 2. EXTRAER COORDENADAS
    # -------------------------

    coords = np.array([
        [
            p["coordinates"]["lat"],
            p["coordinates"]["lng"]
        ]
        for p in places
    ])

    # -------------------------
    # 3. CLUSTERING (IA)
    # -------------------------

    kmeans = KMeans(
        n_clusters=days,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(coords)

    # -------------------------
    # 4. AGRUPAR POR CLUSTER
    # -------------------------

    clusters = {}

    for label, place in zip(labels, places):

        if label not in clusters:
            clusters[label] = []

        clusters[label].append(place)

    # -------------------------
    # 5. CREAR ITINERARIO POR DÍA
    # -------------------------

    itinerary = []

    for day in range(days):

        day_places = clusters.get(day, [])

        day_places = sort_by_real_path(day_places)

        # ordenar por relevancia dentro del cluster
        day_places = sorted(
            day_places,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        remaining = hours_per_day
        final_day = []
        
        MAX_DISTANCE_KM = 5
        
        for place in day_places:
        
            if len(final_day) > 0:
            
                previous = final_day[-1]
        
                dist = haversine(
                    (
                        previous["coordinates"]["lat"],
                        previous["coordinates"]["lng"]
                    ),
                    (
                        place["coordinates"]["lat"],
                        place["coordinates"]["lng"]
                    )
                )
        
                if dist > MAX_DISTANCE_KM:
                    continue
                
            if place["duration"] <= remaining:
            
                final_day.append(place)
                remaining -= place["duration"]

        itinerary.append(final_day)

    return itinerary