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

        if st.button("🤖  Generate Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                summary = summarize_pdf(file_path)
            st.success("Summary ready!")
            st.write(summary)

        st.divider()

        question = st.text_input("Ask something about this document", placeholder="Type your question here...")
        if st.button("Ask AI →", use_container_width=True):
            if question:
                with st.spinner("Thinking..."):
                    answer = ask_question(file_path, question)
                st.write(answer)
            else:
                st.warning("Please enter a question first.")