from groq import Groq
import os

client = Groq(api_key="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")


def generate_summary(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Summarize this for a college student:\n{text}"}
        ],
    )
    return response.choices[0].message.content


def generate_questions(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Generate 5 viva questions with answers from:\n{text}"}
        ],
    )
    return response.choices[0].message.content


def generate_flashcards(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Create flashcards (Q/A format) from:\n{text}"}
        ],
    )
    return response.choices[0].message.content

def chat_with_notes(text, user_query):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study assistant. Answer ONLY from the provided notes."
            },
            {
                "role": "user",
                "content": f"Notes:\n{text[:3000]}\n\nQuestion:\n{user_query}"
            }
        ],
    )
    return response.choices[0].message.content