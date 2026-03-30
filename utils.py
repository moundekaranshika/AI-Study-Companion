from groq import Groq
import os
import requests

# Initialize Groq client
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🔹 AI FUNCTIONS

def generate_summary(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Summarize this for a college student:\n{text[:3000]}"}
        ],
    )
    return response.choices[0].message.content


def generate_questions(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Generate 5 viva questions with answers from:\n{text[:3000]}"}
        ],
    )
    return response.choices[0].message.content


def generate_flashcards(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Create flashcards (Q/A format) from:\n{text[:3000]}"}
        ],
    )
    return response.choices[0].message.content


def chat_with_notes(text, user_query):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer only from the given notes."},
            {"role": "user", "content": f"Notes:\n{text[:3000]}\n\nQuestion:\n{user_query}"}
        ],
    )
    return response.choices[0].message.content


# 🔹 OCR API FUNCTION

def ocr_space_api(image_bytes):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': os.getenv("OCR_API_KEY"),
        'language': 'eng',
        'isOverlayRequired': False
    }

    files = {
        'file': ('image.png', image_bytes, 'image/png')
    }

    response = requests.post(url, files=files, data=payload)
    result = response.json()

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return ""
