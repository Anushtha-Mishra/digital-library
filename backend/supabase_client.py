# backend/supabase_client.py
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env file so environment variables are available
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(
        f"⚠️ **Cannot connect to Supabase** — `{e}`\n\n"
        "Your `SUPABASE_URL` in `.env` is invalid or unreachable.\n\n"
        "👉 Go to [Supabase Dashboard → Settings → API](https://supabase.com/dashboard) "
        "and copy your real **Project URL** into `.env`."
    )
    st.stop()