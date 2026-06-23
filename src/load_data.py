import json

def load_places():
    with open("data/tokyo.json", encoding="utf-8") as f:
        return json.load(f)