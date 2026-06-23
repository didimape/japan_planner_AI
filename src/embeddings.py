from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def poi_to_text(poi):
    return f"""
    {poi["name"]}
    {poi["category"]}
    {poi["district"]}
    {' '.join(poi["tags"])}
    {poi["description"]}
    """


def create_embeddings(places):
    texts = [poi_to_text(p) for p in places]
    embeddings = model.encode(texts)

    np.save(
        "models/embeddings.npy",
        embeddings
    )

    return embeddings