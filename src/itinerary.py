import numpy as np
from sklearn.cluster import KMeans

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

        # ordenar por relevancia dentro del cluster
        day_places = sorted(
            day_places,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        remaining = hours_per_day
        final_day = []

        for place in day_places:

            if place["duration"] <= remaining:

                final_day.append(place)
                remaining -= place["duration"]

        itinerary.append(final_day)

    return itinerary