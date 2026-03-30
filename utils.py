import requests
import streamlit as st

API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"


def call_ai(prompt):
    try:
        response = requests.post(
            url=URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"Error: {str(e)}"
