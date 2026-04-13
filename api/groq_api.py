from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file with override=True to catch key changes immediately
load_dotenv(override=True)

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or "gsk_" not in api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except:
        return None

def groq_request(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    client = get_groq_client()
    if not client:
        return "❌ GROQ_API_KEY is missing or invalid in your .env file."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg or "authentication" in error_msg:
            return "❌ Invalid Groq API Key. Please check your .env file."
        if "rate_limit" in error_msg:
            return "❌ AI rate limit reached. Please wait a moment."
        if "connection" in error_msg or "getaddrinfo" in error_msg:
            return "❌ Network Error: Could not connect to AI services."
        return f"❌ AI Error: {str(e)}"

def generate_summary(text: str) -> str:
    prompt = f"Summarize the following text in clear, concise bullet points:\n\n{text[:4000]}"
    return groq_request(prompt)

def ask_question(text: str, question: str) -> str:
    prompt = (
        f"You are a helpful assistant. Answer the question based ONLY on the provided text.\n\n"
        f"Text:\n{text[:4000]}\n\n"
        f"Question: {question}"
    )
    return groq_request(prompt)