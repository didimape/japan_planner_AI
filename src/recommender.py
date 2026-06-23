import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


def cosine(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

def recommend(
        query,
        places,
        embeddings,
        top_k = 20
):
    query_vec = model.encode([query])[0]

    scores = []

    for places, emb in zip(
        places,
        embeddings
    ):
        score = cosine(
            query_vec,
            emb
        )

        place_copy = places.copy()
        place_copy["score"] = score

        scores.append((place_copy, score))

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:top_k]