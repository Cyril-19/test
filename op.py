import streamlit as st
import cv2
import base64
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv

# OpenAI API Key
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

def encode_image(pil_image):
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def send_to_openai(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "extract the text in the image as it is without any additions"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    if "choices" in response_data:
            content = response_data["choices"][0]["message"]["content"]
            usage = response_data.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            cost_per_token = 0.00002  # Example cost per token
            total_cost = total_tokens * cost_per_token
            return content, total_cost
    else:
            return "No text extracted from the image.", 0
