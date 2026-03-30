import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_ai(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()['choices'][0]['message']['content']


def generate_summary(text):
    return call_ai(f"Summarize for a student:\n{text[:3000]}")

def generate_questions(text):
    return call_ai(f"Generate 5 viva questions with answers:\n{text[:3000]}")

def generate_flashcards(text):
    return call_ai(f"Create flashcards:\n{text[:3000]}")

def chat_with_notes(text, query):
    return call_ai(f"Notes:\n{text[:3000]}\nQuestion:\n{query}")
