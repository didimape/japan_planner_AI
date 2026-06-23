import numpy as np

from load_data import load_places
from embeddings import create_embeddings
from recommender import recommend
from itinerary import build_itinerary

places = load_places()

embeddings = create_embeddings(
    places
)

query = """
history
gardens
japanese culture
"""

days = 3

recommendations =  recommend(
    query,
    places,
    embeddings
)

itinerary = build_itinerary(
    recommendations,
    days
)

for i, day in enumerate(
    itinerary,
    start=1
):
    print(
        f"\nDAY {i}"
    )

    for place in day:
        print(
            "-",
            place["name"]
        )