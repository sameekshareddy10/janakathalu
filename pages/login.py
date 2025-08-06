import streamlit as st
from auth import register_user, login_user, load_users

# ---- Page config and hide sidebar nav menu ----
st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        section[data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# ---- Initialize session state ----
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "user" not in st.session_state:
    st.session_state["user"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""

# ---- If already logged in ----
if st.session_state["user"]:
    st.success(f"✅ You are already logged in as **{st.session_state['user']}**")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.toast("👋 Logged out", icon="🚪")
        st.switch_page("app.py")

else:
    # ---- LOGIN MODE ----
    if st.session_state.auth_mode == "login":
        st.title("🔐 Welcome to JanaKathalu")
        with st.form("login_form"):
            st.subheader("Login to JanaKathalu")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            success, msg, name = login_user(username, password)
            if success:
                st.session_state["user"] = username
                st.session_state["name"] = name
                st.session_state["tab"] = "Home"
                st.session_state["messages"] = []
                st.session_state["last_loaded_user"] = None
                st.session_state["show_login_toast"] = True
                st.switch_page("app.py")
            else:
                st.error(msg)

        st.info("Don't have an account?")
        if st.button("Register Now"):
            st.session_state.auth_mode = "register"
            st.rerun()

    # ---- REGISTER MODE ----
    elif st.session_state.auth_mode == "register":
        st.title("🔐 Welcome to JanaKathalu")
        with st.form("register_form"):
            st.subheader("Register for JanaKathalu")
            name = st.text_input("Full Name")
            username = st.text_input("Choose Username")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            reg_submit = st.form_submit_button("Register")

        if reg_submit:
            if not name or not username or not password or not confirm:
                st.error("All fields are required.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif username in load_users():
                st.error("Username already exists.")
            else:
                success, msg = register_user(username, name, password)
                if success:
                    st.success(msg)
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(msg)

        st.info("Already have an account?")
        if st.button("Back to Login"):
            st.session_state.auth_mode = "login"
            st.rerun()
