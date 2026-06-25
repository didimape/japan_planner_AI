import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recommend(query, places, embeddings, top_k=30, avoid=None):

    query_vec = model.encode([query])[0]

    results = []

    avoid_words = avoid.lower().split() if avoid else []

    for place, emb in zip(places, embeddings):

        score = cosine(query_vec, emb)

        text = (
            place["name"] + " " +
            place["description"] + " " +
            " ".join(place["tags"])
        ).lower()

        # ❌ PENALIZACIÓN (NO QUIERO ESTO)
        if avoid_words:
            if any(word in text for word in avoid_words):
                score -= 0.5

        # 🎯 BOOSTS (EJEMPLOS PROYECTO)
        if "manga" in query.lower() and "nakano" in text:
            score += 0.4

        if "photography" in query.lower():
            if "tower" in text or "view" in text or "sky" in text:
                score += 0.2

        if "romantic" in query.lower():
            if "park" in text or "garden" in text:
                score += 0.2

        place_copy = place.copy()
        place_copy["score"] = score

        results.append(place_copy)

    results.sort(key=lambda x: x["score"], reverse=True)

    return [(p, p["score"]) for p in results[:top_k]]