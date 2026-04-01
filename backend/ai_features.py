import pdfplumber
from api.groq_api import generate_summary


def extract_text(pdf_path):
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:5]:  # only first 5 pages
                text += page.extract_text() or ""
    except:
        return ""

    return text


def chunk_text(text, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_pdf(pdf_path):
    text = extract_text(pdf_path)

    if not text.strip():
        return "❌ No readable text found"

    chunks = chunk_text(text)

    final_summary = ""

    for chunk in chunks[:2]:
        try:
            summary = generate_summary(chunk)
            final_summary += summary + "\n\n"
        except:
            return "❌ AI failed"

    return final_summary


def ask_question(pdf_path, question):
    text = extract_text(pdf_path)

    if not text.strip():
        return "❌ No readable text found"

    try:
        prompt = f"Answer this question based on the text:\n\n{text[:2000]}\n\nQuestion: {question}"
        response = generate_summary(prompt)
        return response
    except:
        return "❌ AI failed"