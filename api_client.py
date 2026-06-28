from __future__ import print_function, unicode_literals
import base64
import json
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, VISION_MODEL


def _headers():
    return {
        "Authorization": "Bearer " + OPENAI_API_KEY,
        "Content-Type": "application/json",
    }


def chat_completion(messages, model=None, response_json=True):
    if model is None:
        model = OPENAI_MODEL
    body = {
        "model": model,
        "messages": messages,
    }
    if response_json:
        body["response_format"] = {"type": "json_object"}

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=_headers(),
        json=body,
        timeout=120,
    )
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    if response_json:
        return json.loads(content)
    return content


def analyze_image_vision(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Analyze this image for microstock metadata. "
                        "Return ONLY valid JSON with these keys: "
                        "subject, objects (array), colors (array), mood, concept, "
                        "industry, categories (array), commercial_uses (array), "
                        "location, season, copy_space, background_type, orientation"
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64," + b64},
                },
            ],
        }
    ]

    return chat_completion(messages, model=VISION_MODEL)
