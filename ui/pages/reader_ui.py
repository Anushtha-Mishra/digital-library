import streamlit as st
import os
import webbrowser
from backend.ai_features import summarize_pdf, ask_question
from backend.db_helpers import get_user_pdfs, get_summary, save_summary, save_chat, get_chat_history


def show_reader():
    folder = "data/books"

    if not os.path.exists(folder) or not os.listdir(folder):
        st.info("Your library is empty. Upload a PDF to get started.")
        return

    files = os.listdir(folder)
    selected_file = st.selectbox("Select a document", files)

    if selected_file:
        file_path = os.path.join(folder, selected_file)

        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥  Download PDF",
                pdf_bytes,
                file_name=selected_file,
                use_container_width=True
            )
        with col2:
            if st.button("📖  Open PDF", use_container_width=True, key="open_pdf_btn"):
                webbrowser.open(file_path)

        st.divider()

        if st.button("🤖  Generate Summary", use_container_width=True, key="reader_sum_btn"):
            with st.spinner("⏳ AI is reading and summarizing..."):
                summary = summarize_pdf(file_path)
            if summary.startswith("❌"):
                st.error(summary)
            else:
                st.success("✅ Summary ready!")
                st.markdown(f"""
                <div style="background:var(--surface);border:1px solid var(--border2);
                    border-radius:12px;padding:20px;margin-top:10px;font-size:14px;line-height:1.7;">
                    {summary}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        st.markdown("💬 **Ask anything about this document**")
        question = st.text_input("Question", placeholder="e.g. What is the budget summary?", label_visibility="collapsed")
        if st.button("🚀 Ask AI →", use_container_width=True, key="reader_ask_btn"):
            if question:
                with st.spinner("🧠 AI is thinking..."):
                    answer = ask_question(file_path, question)
                if answer.startswith("❌"):
                    st.error(answer)
                else:
                    st.info("🤖 AI Answer")
                    st.write(answer)
            else:
                st.warning("⚠️ Please enter a question first.")