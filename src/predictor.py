import joblib

model = joblib.load("models/preference_model.pkl")


def predict_preferences(text):
    prediction = model.predict([text])[0]
    return prediction