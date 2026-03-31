import requests
import streamlit as st

API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
OCR_KEY = st.secrets.get("OCR_API_KEY", "")

URL = "https://openrouter.ai/api/v1/chat/completions"


# 🔹 AI CALL
def call_ai(prompt):
    try:
        response = requests.post(
            url=URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openchat/openchat-7b:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = response.json()

        if "choices" not in data:
            return f"API Error: {data}"

        return data['choices'][0]['message']['content']

    except Exception as e:
        return f"Error: {str(e)}"


# 🔹 FEATURES
def generate_summary(text):
    return call_ai(f"Summarize for a student:\n{text[:3000]}")


def generate_questions(text):
    return call_ai(f"Generate 5 viva questions with answers:\n{text[:3000]}")


def generate_flashcards(text):
    return call_ai(f"Create flashcards:\n{text[:3000]}")


def chat_with_notes(text, query):
    return call_ai(f"Notes:\n{text[:3000]}\nQuestion:\n{query}")


# 🔹 OCR
def ocr_space_api(image_bytes):
    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": ("image.png", image_bytes)},
            data={"apikey": OCR_KEY}
        )

        result = response.json()

        if "ParsedResults" in result:
            return result["ParsedResults"][0]["ParsedText"]

        return ""

    except:
        return ""
