import os
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------
# CARGAR DATASET
# -------------------------

df = pd.read_csv("data/training_data.csv")

X = df["text"]
y = df["label"]

# -------------------------
# CREAR MODELO
# -------------------------

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# -------------------------
# ENTRENAR
# -------------------------

model.fit(X, y)

# -------------------------
# GUARDAR
# -------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/preference_model.pkl"
)

print("Modelo entrenado correctamente.")