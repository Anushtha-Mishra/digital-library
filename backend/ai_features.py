import pdfplumber
from api.groq_api import generate_summary, ask_question as groq_ask


def extract_text(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:10]:  # Read up to 10 pages for better context
                text += page.extract_text() or ""
    except Exception as e:
        return f"❌ Error reading PDF: {str(e)}"
    return text


def summarize_pdf(pdf_path):
    text = extract_text(pdf_path)
    if not text.strip() or text.startswith("❌"):
        return text if text.startswith("❌") else "❌ No readable text found in PDF"
    
    return generate_summary(text)


def ask_question(pdf_path, question):
    text = extract_text(pdf_path)
    if not text.strip() or text.startswith("❌"):
        return text if text.startswith("❌") else "❌ No readable text found in PDF"
    
    return groq_ask(text, question)