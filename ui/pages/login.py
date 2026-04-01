import streamlit as st
from backend.auth import sign_in, sign_up

def show_login():
    st.title("🔐 Login / Signup")

    choice = st.radio("Choose", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            res = sign_up(email, password)
            st.success("Account created!")

    else:
        if st.button("Login"):
            res = sign_in(email, password)
            
            if hasattr(res, "user"):
                st.success("Login successful!")
                st.session_state["user"] = res.user.email
            else:
                st.error("Login failed")