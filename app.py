import streamlit as st
from ui.pages.reader_ui import show_reader
from ui.pages.upload import show_upload
from backend.auth import show_auth_page, sign_out, get_current_user

st.set_page_config(
    page_title="DiLib — Digital Library",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = ["🏠  Home", "📤  Upload", "📚  Library", "🤖  Summarize", "💬  Ask AI"]

if "nav" not in st.session_state:
    st.session_state.nav = "🏠  Home"
if "user" not in st.session_state:
    st.session_state.user = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None


# ── Navigation callbacks ──
def nav_to(page):
    st.session_state.nav = page
    st.session_state.sidebar_nav = page

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap');

:root {
    --bg:       #080A0F;
    --bg2:      #0E1118;
    --surface:  #13171F;
    --surface2: #1C2130;
    --border:   rgba(255,255,255,0.06);
    --border2:  rgba(255,255,255,0.12);
    --gold:     #D4A847;
    --gold-dim: rgba(212,168,71,0.12);
    --red:      #C9463F;
    --blue:     #3B7DD8;
    --text:     #E4E8F0;
    --muted:    #5A6070;
    --muted2:   #8892A4;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="manage-app-button"] { display: none !important; }
.block-container { padding-top: 0 !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; background: transparent !important; }
[data-testid="stSidebar"] section { padding: 0 !important; }
[data-testid="stSidebar"] .stRadio { margin: 0 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div {
    display: flex !important; flex-direction: column !important;
    gap: 0 !important; padding: 0 !important;
}
[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none !important; width: 0 !important; height: 0 !important; position: absolute !important;
}
[data-testid="stSidebar"] .stRadio label span:first-child,
[data-testid="stSidebar"] .stRadio [class*="radioMark"] { display: none !important; }
[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important;
    padding: 13px 22px !important; margin: 0 !important;
    border-radius: 0 !important; cursor: pointer !important;
    transition: background 0.15s ease, color 0.15s ease !important;
    border: none !important; border-left: 3px solid transparent !important;
    background: transparent !important; font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important; font-weight: 500 !important;
    color: #C8CDD8 !important; letter-spacing: 0.01em !important;
    width: 100% !important; box-sizing: border-box !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.06) !important;
    color: #ffffff !important;
    border-left: 3px solid rgba(212,168,71,0.3) !important;
}
[data-testid="stSidebar"] .stRadio label:has(> input:checked) {
    background: rgba(212,168,71,0.10) !important;
    color: #D4A847 !important; font-weight: 600 !important;
    border-left: 3px solid #D4A847 !important;
}
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stRadio label > div > p,
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] .stRadio label * {
    margin: 0 !important; font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important; font-weight: 500 !important;
    color: inherit !important; line-height: 1.2 !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 0 !important; }

/* BUTTONS */
.stButton > button,
.stDownloadButton > button,
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #8892A4 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13.5px !important; font-weight: 500 !important;
    padding: 9px 20px !important;
    transition: all 0.18s ease !important;
    letter-spacing: 0.02em !important; box-shadow: none !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(212,168,71,0.12) !important;
    color: #D4A847 !important;
    border-color: rgba(212,168,71,0.45) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active,
.stDownloadButton > button:active { transform: translateY(0) !important; }

/* INPUTS */
.stSelectbox > div > div {
    background: var(--surface) !important; border: 1px solid var(--border2) !important;
    border-radius: 10px !important; color: var(--text) !important;
}
.stTextInput > div > div > input {
    background: var(--surface) !important; border: 1px solid var(--border2) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-size: 14px !important; padding: 10px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(212,168,71,0.5) !important;
    box-shadow: 0 0 0 2px rgba(212,168,71,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }
.stTextArea textarea {
    background: var(--surface) !important; border: 1px solid var(--border2) !important;
    border-radius: 10px !important; color: var(--text) !important;
}
[data-testid="stFileUploader"] {
    background: var(--surface) !important; border: 1px dashed var(--border2) !important;
    border-radius: 12px !important;
}
div[role="listbox"] { background: var(--surface2) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; }
div[role="option"] { color: var(--text) !important; }
div[role="option"]:hover { background: var(--gold-dim) !important; color: var(--gold) !important; }
.stSelectbox label, .stTextInput label, .stTextArea label {
    color: var(--muted2) !important; font-size: 13px !important; font-weight: 500 !important;
}

/* HOME */
.main-pad { padding: 36px 44px; }
.hero {
    position: relative; overflow: hidden; border-radius: 20px;
    border: 1px solid var(--border2); background: var(--surface);
    padding: 56px 60px; margin-bottom: 24px;
}
.hero::before {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 380px; height: 380px; border-radius: 50%;
    background: radial-gradient(circle, rgba(212,168,71,0.09) 0%, transparent 68%);
    pointer-events: none;
}
.hero::after {
    content: ''; position: absolute; bottom: -60px; left: 60px;
    width: 280px; height: 280px; border-radius: 50%;
    background: radial-gradient(circle, rgba(59,125,216,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 10.5px; font-weight: 600; letter-spacing: 0.20em;
    text-transform: uppercase; color: var(--gold); margin-bottom: 22px;
    display: flex; align-items: center; gap: 10px;
}
.hero-eyebrow::before {
    content: ''; display: inline-block; width: 28px; height: 1px;
    background: var(--gold); opacity: 0.7;
}
.hero-h1 {
    font-family: 'Playfair Display', serif; font-size: 56px; font-weight: 900;
    line-height: 1.06; letter-spacing: -0.03em; color: #fff; margin: 0 0 20px;
}
.hero-h1 em { font-style: italic; color: var(--gold); }
.hero-sub {
    font-size: 15px; font-weight: 300; color: var(--muted2);
    line-height: 1.8; max-width: 500px; margin-bottom: 44px;
}
.hero-stats { display: flex; gap: 52px; flex-wrap: wrap; }
.hstat-n { font-family: 'Playfair Display', serif; font-size: 34px; font-weight: 700; color: var(--gold); line-height: 1; }
.hstat-l { font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin-top: 5px; }

.feat-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 28px 26px 24px;
    position: relative; overflow: hidden;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    margin-bottom: 8px;
}
.feat-card:hover {
    border-color: rgba(212,168,71,0.45);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(212,168,71,0.08);
}
.feat-num {
    position: absolute; top: 14px; right: 20px;
    font-family: 'Playfair Display', serif; font-size: 64px; font-weight: 900;
    color: rgba(255,255,255,0.025); line-height: 1; user-select: none;
}
.feat-dot { width: 9px; height: 9px; border-radius: 50%; margin-bottom: 22px; }
.dot-gold { background: #D4A847; }
.dot-red  { background: #C9463F; }
.dot-blue { background: #3B7DD8; }
.feat-title {
    font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700;
    color: #fff; margin-bottom: 10px; letter-spacing: -0.01em;
}
.feat-desc { font-size: 13.5px; font-weight: 300; color: var(--muted2); line-height: 1.72; }

/* Card nav buttons — prominent gold buttons */
[data-testid="column"] .stButton > button {
    background: linear-gradient(135deg, rgba(212,168,71,0.18) 0%, rgba(212,168,71,0.08) 100%) !important;
    color: #D4A847 !important;
    border: 1px solid rgba(212,168,71,0.35) !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important; font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    padding: 12px 20px !important; width: 100% !important;
    box-shadow: 0 2px 8px rgba(212,168,71,0.08) !important;
    transition: all 0.20s ease !important;
    cursor: pointer !important;
}
[data-testid="column"] .stButton > button:hover {
    background: linear-gradient(135deg, rgba(212,168,71,0.30) 0%, rgba(212,168,71,0.15) 100%) !important;
    border-color: rgba(212,168,71,0.60) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(212,168,71,0.18) !important;
}

.banner {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 32px 38px;
    display: flex; align-items: center; justify-content: space-between;
    gap: 28px; flex-wrap: wrap; margin-top: 20px;
}
.banner h3 {
    font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700;
    color: #fff; margin: 0 0 8px; letter-spacing: -0.01em;
}
.banner p { font-size: 13.5px; font-weight: 300; color: var(--muted2); margin: 0; line-height: 1.65; }
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; }
.tag {
    background: rgba(255,255,255,0.04); border: 1px solid var(--border2);
    border-radius: 999px; padding: 6px 14px;
    font-size: 12px; font-weight: 500; color: var(--muted2);
}
.tag.gt { background: var(--gold-dim); border-color: rgba(212,168,71,0.28); color: var(--gold); }

.pg-head { padding: 36px 44px 0; }
.pg-title {
    font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 900;
    color: #fff; letter-spacing: -0.02em; margin-bottom: 8px;
}
.pg-div { width: 38px; height: 2px; background: var(--gold); border-radius: 2px; margin-bottom: 6px; }
.pg-sub { font-size: 14px; font-weight: 300; color: var(--muted); margin-bottom: 28px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:30px 22px 20px;">
      <div style="display:flex;align-items:center;gap:11px;">
        <div style="width:38px;height:38px;border-radius:11px;
          background:rgba(212,168,71,0.12);border:1px solid rgba(212,168,71,0.28);
          display:flex;align-items:center;justify-content:center;font-size:18px;">📚</div>
        <div>
          <div style="font-family:'Playfair Display',serif;font-size:19px;
            font-weight:900;color:#fff;letter-spacing:-0.02em;line-height:1.1;">DiLib</div>
          <div style="font-size:9.5px;color:#6B7585;letter-spacing:0.14em;
            text-transform:uppercase;font-weight:600;margin-top:1px;">Digital Library</div>
        </div>
      </div>
    </div>
    <div style="padding:0 22px 14px;">
      <div style="background:rgba(212,168,71,0.07);border:1px solid rgba(212,168,71,0.18);
        border-radius:10px;padding:10px 14px;display:flex;align-items:center;gap:8px;">
        <div style="width:7px;height:7px;border-radius:50%;background:#D4A847;flex-shrink:0;"></div>
        <span style="font-size:12px;color:#D4A847;font-weight:500;">AI Engine Active</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:12px 22px 10px;border-top:1px solid rgba(255,255,255,0.06);
        border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:4px;">
      <div style="font-size:9.5px;font-weight:700;letter-spacing:0.16em;
          text-transform:uppercase;color:#6B7585;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.radio(
        "", PAGES,
        index=PAGES.index(st.session_state.nav),
        key="sidebar_nav",
        label_visibility="collapsed",
    )
    if selected != st.session_state.nav:
        st.session_state.nav = selected
        st.rerun()

    user = get_current_user()
    if user:
        st.markdown(f"""
        <div style="padding:16px 22px 0;border-top:1px solid rgba(255,255,255,0.06);margin-top:16px;">
          <div style="font-size:9.5px;font-weight:700;letter-spacing:0.16em;
              text-transform:uppercase;color:#6B7585;margin-bottom:10px;">Logged in as</div>
          <div style="font-size:12px;color:#C8CDD8;word-break:break-all;">{user.email}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪  Logout", key="btn_logout", use_container_width=True):
            sign_out()

    st.markdown("""
    <div style="padding:20px 22px 0;border-top:1px solid rgba(255,255,255,0.06);margin-top:16px;">
      <div style="font-size:9.5px;font-weight:700;letter-spacing:0.16em;
          text-transform:uppercase;color:#6B7585;margin-bottom:14px;">System Info</div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:12px;color:#8892A4;">Version</span>
          <span style="font-size:11px;color:#8892A4;background:rgba(255,255,255,0.06);
            padding:2px 9px;border-radius:999px;border:1px solid rgba(255,255,255,0.1);">v1.0</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:12px;color:#8892A4;">PDF Q&A</span>
          <span style="font-size:12px;color:#D4A847;font-weight:600;">Enabled</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:12px;color:#8892A4;">Summaries</span>
          <span style="font-size:12px;color:#D4A847;font-weight:600;">Enabled</span>
        </div>
      </div>
    </div>
    <div style="padding:20px 22px 28px;margin-top:20px;">
      <div style="background:rgba(212,168,71,0.05);border:1px solid rgba(212,168,71,0.14);
        border-radius:12px;padding:16px;">
        <div style="font-size:11px;color:#D4A847;font-weight:600;
            letter-spacing:0.04em;margin-bottom:6px;">✦ Pro Tip</div>
        <div style="font-size:12px;color:#8892A4;line-height:1.65;">
          Upload any PDF and ask questions directly — AI answers instantly from your document content.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── AUTH GATE ──
if not get_current_user():
    show_auth_page()
    st.stop()

# ── HOME ──
if st.session_state.nav == "🏠  Home":
    st.markdown("""
    <div class="main-pad">
      <div class="hero">
        <div class="hero-eyebrow">AI-Powered Reading System</div>
        <h1 class="hero-h1">Your Personal<br><em>Reading Universe</em></h1>
        <p class="hero-sub">
          Upload PDFs, generate instant AI summaries, and have real conversations
          with your documents — all inside one seamless, elegant workspace.
        </p>
        <div class="hero-stats">
          <div><div class="hstat-n">∞</div><div class="hstat-l">Documents</div></div>
          <div><div class="hstat-n">AI</div><div class="hstat-l">Powered</div></div>
          <div><div class="hstat-n">⚡</div><div class="hstat-l">Instant Q&A</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-num">01</div>
          <div class="feat-dot dot-gold"></div>
          <div class="feat-title">Upload PDFs</div>
          <p class="feat-desc">Add books, research papers, notes, and any document.
          Your library — always organized and searchable.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("📤  Go to Upload →", key="btn_upload", use_container_width=True,
                  on_click=nav_to, args=("📤  Upload",))

    with c2:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-num">02</div>
          <div class="feat-dot dot-red"></div>
          <div class="feat-title">AI Summaries</div>
          <p class="feat-desc">Get crisp, accurate summaries of any uploaded PDF.
          Save hours — understand the key ideas instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("🤖  Get Summaries →", key="btn_summary", use_container_width=True,
                  on_click=nav_to, args=("🤖  Summarize",))

    with c3:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-num">03</div>
          <div class="feat-dot dot-blue"></div>
          <div class="feat-title">Ask Questions</div>
          <p class="feat-desc">Ask anything from your document and receive
          context-aware answers in real time. Like a personal tutor.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("💬  Ask AI Questions →", key="btn_ask", use_container_width=True,
                  on_click=nav_to, args=("💬  Ask AI",))

    st.markdown("""
    <div style="padding: 4px 44px 36px;">
      <div class="banner">
        <div>
          <h3>Why this stands out</h3>
          <p>Combines document management with a powerful AI reading layer.<br>
             Passive documents become interactive, conversational knowledge.</p>
        </div>
        <div class="tag-row">
          <span class="tag gt">⚡ Instant Upload</span>
          <span class="tag gt">🧠 AI Summaries</span>
          <span class="tag">📖 PDF Reader</span>
          <span class="tag">💬 Doc Q&A</span>
          <span class="tag">🔍 Smart Search</span>
          <span class="tag">🌙 Dark Mode</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── UPLOAD ──
elif st.session_state.nav == "📤  Upload":
    st.markdown("""
    <div class="pg-head">
      <div class="pg-title">Upload Documents</div>
      <div class="pg-div"></div>
      <p class="pg-sub">Add PDFs to your personal library — books, notes, research papers, anything.</p>
    </div>
    """, unsafe_allow_html=True)
    show_upload()

# ── LIBRARY ──
elif st.session_state.nav == "📚  Library":
    st.markdown("""
    <div class="pg-head">
      <div class="pg-title">Your Library</div>
      <div class="pg-div"></div>
      <p class="pg-sub">Browse, read, summarize, and chat with your uploaded documents.</p>
    </div>
    """, unsafe_allow_html=True)
    show_reader()

# ── SUMMARIZE ──
elif st.session_state.nav == "🤖  Summarize":
    st.markdown("""
    <div class="pg-head">
      <div class="pg-title">AI Summarizer</div>
      <div class="pg-div"></div>
      <p class="pg-sub">Select any PDF from your library and get an instant AI-generated summary.</p>
    </div>
    """, unsafe_allow_html=True)

    import os
    from backend.ai_features import summarize_pdf

    folder = "data/books"
    if not os.path.exists(folder) or not os.listdir(folder):
        st.info("📭 Your library is empty. Upload a PDF first to generate summaries.")
        st.button("📤  Go to Upload", key="sum_go_upload", use_container_width=False,
                  on_click=nav_to, args=("📤  Upload",))
    else:
        files = os.listdir(folder)
        selected_file = st.selectbox("📄 Select a document to summarize", files, key="sum_select")

        if selected_file:
            file_path = os.path.join(folder, selected_file)

            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border2);
                border-radius:12px;padding:18px 22px;margin:12px 0 20px;">
              <div style="font-size:13px;color:var(--muted2);">Selected Document</div>
              <div style="font-size:16px;color:#fff;font-weight:600;margin-top:4px;">📄 {selected_file}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🤖  Generate AI Summary", key="btn_gen_summary", use_container_width=True):
                with st.spinner("⏳ AI is reading and summarizing your document..."):
                    summary = summarize_pdf(file_path)
                st.success("✅ Summary generated!")
                st.markdown(f"""
                <div style="background:var(--surface);border:1px solid var(--border2);
                    border-radius:14px;padding:24px 28px;margin-top:16px;">
                  <div style="font-size:11px;color:var(--gold);font-weight:700;
                      letter-spacing:0.12em;text-transform:uppercase;margin-bottom:14px;">
                    🤖 AI Summary
                  </div>
                  <div style="font-size:14px;color:var(--text);line-height:1.8;white-space:pre-wrap;">
{summary}
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ── ASK AI ──
elif st.session_state.nav == "💬  Ask AI":
    st.markdown("""
    <div class="pg-head">
      <div class="pg-title">Ask AI Questions</div>
      <div class="pg-div"></div>
      <p class="pg-sub">Select a document and ask any question — AI will answer from your PDF content.</p>
    </div>
    """, unsafe_allow_html=True)

    import os
    from backend.ai_features import ask_question

    folder = "data/books"
    if not os.path.exists(folder) or not os.listdir(folder):
        st.info("📭 Your library is empty. Upload a PDF first to ask questions.")
        st.button("📤  Go to Upload", key="ask_go_upload", use_container_width=False,
                  on_click=nav_to, args=("📤  Upload",))
    else:
        files = os.listdir(folder)
        selected_file = st.selectbox("📄 Select a document", files, key="ask_select")

        if selected_file:
            file_path = os.path.join(folder, selected_file)

            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border2);
                border-radius:12px;padding:18px 22px;margin:12px 0 20px;">
              <div style="font-size:13px;color:var(--muted2);">Selected Document</div>
              <div style="font-size:16px;color:#fff;font-weight:600;margin-top:4px;">📄 {selected_file}</div>
            </div>
            """, unsafe_allow_html=True)

            question = st.text_input("💬 Ask something about this document",
                                     placeholder="e.g. What is the main conclusion of this paper?",
                                     key="ask_question_input")

            if st.button("🚀  Ask AI →", key="btn_ask_ai", use_container_width=True):
                if question:
                    with st.spinner("🧠 AI is thinking..."):
                        answer = ask_question(file_path, question)
                    st.markdown(f"""
                    <div style="background:var(--surface);border:1px solid var(--border2);
                        border-radius:14px;padding:24px 28px;margin-top:16px;">
                      <div style="font-size:11px;color:var(--gold);font-weight:700;
                          letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;">
                        💬 Your Question
                      </div>
                      <div style="font-size:14px;color:var(--muted2);margin-bottom:18px;
                          font-style:italic;">"{question}"</div>
                      <div style="height:1px;background:var(--border2);margin-bottom:18px;"></div>
                      <div style="font-size:11px;color:var(--gold);font-weight:700;
                          letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;">
                        🤖 AI Answer
                      </div>
                      <div style="font-size:14px;color:var(--text);line-height:1.8;white-space:pre-wrap;">
{answer}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Please type a question first.")