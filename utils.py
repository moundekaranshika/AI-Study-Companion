from google import genai
import streamlit as st
import requests

# Configure client
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])


# 🔹 AI CALL
def call_ai(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
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
            data={"apikey": st.secrets["OCR_API_KEY"]}
        )

        result = response.json()

        if "ParsedResults" in result:
            return result["ParsedResults"][0]["ParsedText"]

        return ""

    except:
        return ""
