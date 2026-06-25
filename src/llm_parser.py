import requests


def extract_preferences(user_text):

    prompt = f"""
You are a travel preference extractor.

Extract user travel preferences.

IMPORTANT RULES:
- Understand NEGATIONS ("no me gusta", "I don't like", "evitar")
- Separate interests and dislikes clearly
- Do NOT include disliked topics in interests

Return format EXACTLY like this:

INTERESTS: keyword1 keyword2 keyword3
AVOID: keyword1 keyword2

User text:
{user_text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()