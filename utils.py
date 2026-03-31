import google.generativeai as genai
import streamlit as st
import requests

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash-latest")


# 🔹 AI CALL
def call_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# 🔹 FEATURES
def generate_summary(text):
    return call_ai(f"Summarize this for a college student:\n{text[:3000]}")


def generate_questions(text):
    return call_ai(f"Generate 5 viva questions with answers:\n{text[:3000]}")


def generate_flashcards(text):
    return call_ai(f"Create flashcards (Q/A format):\n{text[:3000]}")


def chat_with_notes(text, query):
    return call_ai(f"Answer ONLY from these notes:\n{text[:3000]}\n\nQuestion:\n{query}")


# 🔹 OCR (same as before)
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
