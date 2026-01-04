import requests
import os

from dotenv import load_dotenv

load_dotenv()


def chat_completions(model: str, prompt: str) -> str:
    base_url = "https://api.openai.com/v1/chat/completions"
    token = os.getenv("OPENAI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are CivicShield MCP, an AI that explains digital rights risks "
                "to activists clearly and without legal jargon.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(base_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # IMPORTANT: always return a STRING
        return (
            "⚠️ Unable to analyze this document right now due to a technical issue. "
            "Please try again later."
        )
