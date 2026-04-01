import streamlit as st
import os
from backend.db_helpers import upload_pdf_to_storage, save_pdf_record


def show_upload():
    st.subheader("📤 Upload PDF")

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        os.makedirs("data/books", exist_ok=True)
        file_path = os.path.join("data/books", uploaded_file.name)

        file_bytes = uploaded_file.read()

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        url, path = upload_pdf_to_storage(file_bytes, uploaded_file.name)
        if url:
            save_pdf_record(uploaded_file.name, url)

        st.success(f"✅ Uploaded: {uploaded_file.name}")








# import streamlit as st
# import os
# from db_helpers import upload_pdf_to_storage, save_pdf_record

# # file upload ke baad:
# url, path = upload_pdf_to_storage(file.read(), file.name)
# if url:
#     save_pdf_record(file.name, url)

# def show_upload():
#     st.subheader("📤 Upload PDF")

#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

#     if uploaded_file is not None:
#         os.makedirs("data/books", exist_ok=True)

#         file_path = os.path.join("data/books", uploaded_file.name)

#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         st.success(f"Uploaded: {uploaded_file.name}")