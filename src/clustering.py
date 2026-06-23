import numpy as np
from sklearn.cluster import KMeans

def cluster_places(
    places,
    n_clusters
):
    coords = np.array([
        [
            p["coordinates"]["lat"],
            p["coordinates"]["lng"]
        ]
        for p in places
    ])

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )

    labels = model.fit_predict(coords)

    return labels