import streamlit as st
from ui.pages.upload import show_upload
from ui.pages.reader_ui import show_reader

def show_dashboard():
    st.title("📚 Digital Library")

    menu = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📤 Upload", "📚 Library"]
    )

    if menu == "🏠 Home":
        st.markdown("### Welcome to your Smart Library 🚀")

        col1, col2, col3 = st.columns(3)

        col1.metric("Upload", "📤")
        col2.metric("Read", "📖")
        col3.metric("Smart", "🤖")

        st.markdown("---")
        st.info("Manage and read your books in one place.")

    elif menu == "📤 Upload":
        show_upload()

    elif menu == "📚 Library":
        show_reader()