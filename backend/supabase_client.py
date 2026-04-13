# backend/supabase_client.py
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env file so environment variables are available
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "⚠️ **Supabase credentials missing!**\n\n"
        "Add these to your `.env` file:\n"
        "```\nSUPABASE_URL=https://xxxx.supabase.co\n"
        "SUPABASE_KEY=your_anon_key_here\n```"
    )
    st.stop()

# Check for placeholder value
if "xxxxxxxxxxxx" in SUPABASE_KEY:
    st.error(
        "⚠️ **Invalid Supabase key detected!**\n\n"
        "Your `.env` file contains a placeholder key (`xxxxxxxxxxxx`).\n\n"
        "👉 Go to [Supabase Dashboard → Settings → API](https://supabase.com/dashboard) "
        "and copy your real **anon public** key into `.env`."
    )
    st.stop()

try:
    if not SUPABASE_URL.startswith("http"):
        raise ValueError(f"Invalid URL protocol. URL starts with: {SUPABASE_URL[:10]}...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    masked_url = f"{SUPABASE_URL[:12]}...{SUPABASE_URL[-5:]}" if SUPABASE_URL else "None"
    st.error(
        f"⚠️ **Cannot connect to Supabase**\n\n"
        f"**Error:** `{e}`\n"
        f"**Detected URL:** `{masked_url}`\n\n"
        "Your `SUPABASE_URL` in Railway is likely incorrect or has a typo.\n"
        "👉 [Go to Supabase Dashboard](https://supabase.com/dashboard) and copy the **Project URL**."
    )
    st.stop()