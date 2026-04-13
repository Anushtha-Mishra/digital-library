import streamlit as st
from backend.supabase_client import supabase


def sign_up(email: str, password: str, full_name: str):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": full_name}}
        })
        if res.user:
            try:
                supabase.table("profiles").upsert({
                    "id": str(res.user.id),
                    "email": email,
                    "full_name": full_name
                }).execute()
            except:
                pass
            # Check if email confirmation is required
            if res.session is None:
                return True, "✅ Account created! Check your email inbox and click the confirmation link to activate your account, then log in."
            return True, "✅ Account created! You can now log in."
        return False, "Signup failed. Please try again."
    except Exception as e:
        err = str(e)
        if "already registered" in err or "already been registered" in err or "already exists" in err.lower():
            return False, "📧 This email is already registered. Please log in instead."
        if "rate limit" in err.lower() or "security purposes" in err.lower() or "too many" in err.lower():
            return False, "⏳ Too many signup attempts. Please wait 60 seconds and try again."
        if "password" in err.lower() and ("short" in err.lower() or "weak" in err.lower() or "characters" in err.lower()):
            return False, "🔒 Password is too weak. Please use at least 6 characters."
        if "timed out" in err.lower() or "ssl" in err.lower() or "getaddrinfo" in err.lower() or "name or service not known" in err.lower():
            from backend.supabase_client import SUPABASE_URL
            masked_url = f"{SUPABASE_URL[:12]}...{SUPABASE_URL[-5:]}" if SUPABASE_URL else "None"
            return False, f"🌐 Connection failed. Check Supabase URL in Railway. (Detected: {masked_url})"
        return False, f"❌ Signup error: {err}"


def sign_in(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if res.user:
            st.session_state.user = res.user
            st.session_state.access_token = res.session.access_token
            return True, "Welcome back!"
        return False, "Incorrect email or password."
    except Exception as e:
        err = str(e).lower()
        if "email not confirmed" in err or "not confirmed" in err:
            return False, "📧 Email not confirmed. Check your inbox and click the confirmation link — or ask admin to disable email confirmation in Supabase dashboard."
        if "invalid login" in err or "invalid credentials" in err or "wrong password" in err:
            return False, "❌ Incorrect email or password."
        if "user not found" in err or "no user found" in err:
            return False, "❌ No account found with that email. Please sign up first."
        if "timed out" in err or "ssl" in err or "getaddrinfo" in err or "name or service not known" in err:
            from backend.supabase_client import SUPABASE_URL
            masked_url = f"{SUPABASE_URL[:12]}...{SUPABASE_URL[-5:]}" if SUPABASE_URL else "None"
            return False, f"🌐 Connection failed. Check Supabase URL in Railway. (Detected: {masked_url})"
        return False, f"❌ Login failed: {str(e)}"


def sign_out():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.nav = "🏠  Home"
    st.rerun()


def get_current_user():
    return st.session_state.get("user", None)


def show_auth_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap');

    [data-testid="stSidebar"]  { display: none !important; }
    [data-testid="stHeader"]   { display: none !important; }
    #MainMenu, footer, header  { visibility: hidden !important; }

    /* ── FORCE DARK BACKGROUND ON ALL CONTAINERS ── */
    .stApp,
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section.main,
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stForm"],
    [data-testid="stExpander"],
    [data-testid="stTabs"] > div,
    [role="tabpanel"],
    .block-container,
    .element-container {
        background-color: transparent !important;
        color: #E4E8F0 !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse 80% 60% at 10% 20%, rgba(212,168,71,0.13) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 90% 80%, rgba(59,125,216,0.10) 0%, transparent 60%),
            radial-gradient(ellipse 100% 100% at 50% 50%, #080A0F 0%, #050709 100%) !important;
        min-height: 100vh !important;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent !important;
        min-height: 100vh !important;
    }

    [data-testid="stMainBlockContainer"], .block-container {
        max-width: 440px !important;
        margin: 0 auto !important;
        padding: 64px 0 40px !important;
        background: transparent !important;
    }

    /* Floating book decorations via CSS */
    [data-testid="stAppViewContainer"]::before {
        content: '📚';
        position: fixed;
        top: 8%; left: 6%;
        font-size: 64px;
        opacity: 0.06;
        transform: rotate(-15deg);
        pointer-events: none;
        z-index: 0;
    }
    [data-testid="stAppViewContainer"]::after {
        content: '📖';
        position: fixed;
        bottom: 12%; right: 8%;
        font-size: 80px;
        opacity: 0.05;
        transform: rotate(12deg);
        pointer-events: none;
        z-index: 0;
    }

    /* ── TABS ── */
    [data-testid="stTabs"] {
        position: relative; z-index: 1;
    }
    [data-testid="stTabs"] button {
        font-family: 'Outfit', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #6B7585 !important;
        padding: 8px 16px !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #D4A847 !important;
        font-weight: 600 !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [role="tablist"] {
        border-bottom: 1px solid rgba(255,255,255,0.07) !important;
        gap: 4px !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [role="tabpanel"] {
        background: transparent !important;
    }

    /* ── INPUTS — VISIBLE TEXT ON DARK BG ── */
    .stTextInput > div > div > input,
    .stTextInput input,
    input[type="text"],
    input[type="password"],
    input[type="email"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        caret-color: #D4A847 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextInput input:focus {
        border-color: rgba(212,168,71,0.50) !important;
        box-shadow: 0 0 0 3px rgba(212,168,71,0.10) !important;
        background: rgba(212,168,71,0.05) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextInput input::placeholder {
        color: #5A6070 !important;
        -webkit-text-fill-color: #5A6070 !important;
        opacity: 1 !important;
    }

    /* Input labels */
    .stTextInput label,
    .stTextInput > label,
    .stTextInput label p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: #8892A4 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
    }

    /* Input wrapper divs */
    .stTextInput > div,
    .stTextInput > div > div {
        background: transparent !important;
    }

    /* ── SIGN IN BUTTON ── */
    .stButton > button {
        background: linear-gradient(135deg, rgba(212,168,71,0.22) 0%, rgba(212,168,71,0.10) 100%) !important;
        color: #D4A847 !important;
        border: 1px solid rgba(212,168,71,0.40) !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        letter-spacing: 0.04em !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(212,168,71,0.32) 0%, rgba(212,168,71,0.18) 100%) !important;
        border-color: rgba(212,168,71,0.65) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(212,168,71,0.18) !important;
    }

    /* ── ALERTS (success/error/warning) ── */
    [data-testid="stAlert"],
    .stAlert,
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 10px !important;
        color: #E4E8F0 !important;
    }
    [data-testid="stAlert"] p,
    .stAlert p {
        color: #E4E8F0 !important;
    }

    /* ── GENERAL TEXT ── */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Brand header
    st.markdown("""
    <div style="text-align:center; margin-bottom:36px; position:relative; z-index:1;">
      <div style="display:inline-flex;align-items:center;gap:14px;margin-bottom:12px;">
        <div style="
          width:48px;height:48px;border-radius:14px;
          background:linear-gradient(135deg,rgba(212,168,71,0.20),rgba(212,168,71,0.06));
          border:1px solid rgba(212,168,71,0.35);
          display:flex;align-items:center;justify-content:center;
          font-size:22px;
          box-shadow:0 8px 24px rgba(212,168,71,0.12);
        ">📚</div>
        <span style="
          font-family:'Playfair Display',serif;
          font-size:32px;font-weight:900;color:#fff;
          letter-spacing:-0.03em;
        ">DiLib</span>
      </div>
      <div style="
        font-size:9.5px;color:#2A3245;
        letter-spacing:0.22em;text-transform:uppercase;font-weight:600;
      ">Your Personal Digital Library</div>
    </div>
    """, unsafe_allow_html=True)

    # Card
    st.markdown("""
    <div style="
      position:relative; z-index:1;
      background: linear-gradient(160deg, rgba(19,23,31,0.95) 0%, rgba(14,17,24,0.98) 100%);
      border:1px solid rgba(255,255,255,0.08);
      border-radius:24px;
      padding:36px 32px 12px;
      box-shadow:
        0 40px 80px rgba(0,0,0,0.6),
        0 1px 0 rgba(255,255,255,0.05) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset;
      backdrop-filter: blur(20px);
    ">
      <div style="text-align:center; margin-bottom:28px;">
        <div style="
          display:inline-flex;align-items:center;gap:7px;
          background:rgba(212,168,71,0.08);
          border:1px solid rgba(212,168,71,0.16);
          border-radius:999px;padding:5px 14px;
          margin-bottom:20px;
        ">
          <div style="width:5px;height:5px;border-radius:50%;background:#D4A847;
            box-shadow:0 0 6px rgba(212,168,71,0.6);"></div>
          <span style="font-size:10px;font-weight:700;letter-spacing:0.14em;
            text-transform:uppercase;color:#D4A847;">AI-Powered Library</span>
        </div>
        <div style="
          font-family:'Playfair Display',serif;
          font-size:26px;font-weight:700;color:#fff;
          letter-spacing:-0.02em;margin-bottom:10px;
        ">Welcome back</div>
        <div style="font-size:13px;color:#3A4A5A;font-weight:300;line-height:1.6;">
          Sign in to access your personal library
        </div>
      </div>
      <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);margin-bottom:24px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Form — Streamlit renders here
    tab1, tab2 = st.tabs(["🔑  Login", "✨  Sign Up"])

    with tab1:
        email    = st.text_input("Email", key="login_email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", key="btn_login", use_container_width=True):
            if email and password:
                ok, msg = sign_in(email, password)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please fill in both fields.")

    with tab2:
        name   = st.text_input("Full Name",  key="signup_name",  placeholder="Your name")
        email2 = st.text_input("Email",      key="signup_email", placeholder="your@email.com")
        pass2  = st.text_input("Password",   key="signup_pass",  placeholder="Min 6 characters", type="password")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Create Account →", key="btn_signup", use_container_width=True):
            if name and email2 and pass2:
                if len(pass2) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    ok, msg = sign_up(email2, pass2, name)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
            else:
                st.warning("Please fill in all fields.")

    # Card footer
    st.markdown("""
    <div style="
      position:relative; z-index:1;
      background:rgba(14,17,24,0.98);
      border:1px solid rgba(255,255,255,0.08);
      border-top:none;
      border-radius:0 0 24px 24px;
      padding:16px 32px 24px;
      box-shadow:0 40px 80px rgba(0,0,0,0.6);
    ">
      <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.05),transparent);margin-bottom:16px;"></div>
      <div style="text-align:center;font-size:11px;color:#1E2535;letter-spacing:0.02em;">
        🔒 &nbsp; Your documents are private and encrypted
      </div>
    </div>
    """, unsafe_allow_html=True)