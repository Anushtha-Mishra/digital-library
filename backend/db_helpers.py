import streamlit as st
from backend.supabase_client import supabase
import uuid


def get_user_id():
    user = st.session_state.get("user")
    if user:
        return str(user.id)
    return None


# ─── PDF Functions ────────────────────────────────────────

def upload_pdf_to_storage(file_bytes: bytes, file_name: str):
    try:
        user_id = get_user_id()
        path = f"{user_id}/{uuid.uuid4()}_{file_name}"
        supabase.storage.from_("pdfs").upload(
            path,
            file_bytes,
            {"content-type": "application/pdf", "upsert": "true"}
        )
        url = supabase.storage.from_("pdfs").get_public_url(path)
        return url, path
    except Exception as e:
        st.error(f"Upload error: {e}")
        return None, None


def save_pdf_record(file_name: str, storage_url: str):
    try:
        user_id = get_user_id()
        res = supabase.table("pdfs").insert({
            "user_id": user_id,
            "file_name": file_name,
            "storage_url": storage_url
        }).execute()
        return res.data[0]["id"] if res.data else None
    except Exception as e:
        st.error(f"DB save error: {e}")
        return None


def get_user_pdfs() -> list:
    try:
        user_id = get_user_id()
        res = supabase.table("pdfs")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("uploaded_at", desc=True)\
            .execute()
        return res.data or []
    except Exception as e:
        st.error(f"PDFs fetch error: {e}")
        return []


def delete_pdf(pdf_id: str):
    try:
        supabase.table("pdfs").delete().eq("id", pdf_id).execute()
        return True
    except Exception as e:
        st.error(f"Delete error: {e}")
        return False


# ─── Summary Functions ────────────────────────────────────

def save_summary(pdf_id: str, summary_text: str) -> bool:
    try:
        supabase.table("summaries").delete().eq("pdf_id", pdf_id).execute()
        supabase.table("summaries").insert({
            "pdf_id": pdf_id,
            "summary_text": summary_text
        }).execute()
        return True
    except Exception as e:
        st.error(f"Summary save error: {e}")
        return False


def get_summary(pdf_id: str):
    try:
        res = supabase.table("summaries")\
            .select("summary_text")\
            .eq("pdf_id", pdf_id)\
            .execute()
        if res.data:
            return res.data[0]["summary_text"]
        return None
    except:
        return None


# ─── Chat History Functions ───────────────────────────────

def save_chat(pdf_id: str, question: str, answer: str) -> bool:
    try:
        supabase.table("chat_history").insert({
            "pdf_id": pdf_id,
            "question": question,
            "answer": answer
        }).execute()
        return True
    except Exception as e:
        st.error(f"Chat save error: {e}")
        return False


def get_chat_history(pdf_id: str) -> list:
    try:
        res = supabase.table("chat_history")\
            .select("*")\
            .eq("pdf_id", pdf_id)\
            .order("asked_at", desc=False)\
            .execute()
        return res.data or []
    except:
        return []


def clear_chat_history(pdf_id: str) -> bool:
    try:
        supabase.table("chat_history").delete().eq("pdf_id", pdf_id).execute()
        return True
    except:
        return False