import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def chat_reply(user_text: str) -> str:
    """Use Groq (fast & free online model) for responses."""
    try:
        print("[NLP] Using Groq API (fast & free) …")

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # You can switch models: "mixtral-8x7b" or "llama3-8b"
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a concise, helpful voice assistant."},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.6
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        # Check for bad responses
        if response.status_code != 200:
            print(
                f"[NLP] Groq API error: {response.status_code} - {response.text}")
            return "Sorry, Groq service is unavailable."

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"[NLP] Groq error: {e}")
        return "Sorry, I couldn’t reach Groq right now."
