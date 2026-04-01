from groq import Groq
import os

# Railway variable se read karo
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

def generate_summary(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"Summarize this:\n{text[:3000]}"}],
        temperature=0.3
    )
    return response.choices[0].message.content

def ask_question(text, question):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"Text:\n{text[:3000]}\n\nQuestion: {question}"}],
        temperature=0.3
    )
    return response.choices[0].message.content







# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def generate_summary(text):
#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",   # ✅ FINAL MODEL
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"Summarize this in simple bullet points:\n{text[:3000]}"
#             }
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content