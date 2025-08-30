import streamlit as st
from auth import login, logout, get_current_user

def main():
    st.title("🔑 Login Page")

    # If already logged in
    if "access_token" in st.session_state:
        user = get_current_user()
        if user:
            st.success(f"✅ You are already logged in as {user.get('phone')}")
        else:
            st.warning("⚠️ Session expired, please log in again.")

        if st.button("Logout"):
            logout()
            st.info("Logged out successfully")
            st.session_state["user"] = None
            st.session_state["name"] = ""
            st.session_state["tab"] = "Home"
            st.rerun()
        return

    # Login form
    phone = st.text_input("📱 Phone number")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        success, msg = login(phone, password)
        if success:
            st.success(msg)

            # fetch user details immediately after login
            user = get_current_user()
            if user:
                st.session_state["user"] = user.get("phone")
                st.session_state["name"] = user.get("name", "")
            else:
                st.session_state["user"] = phone
                st.session_state["name"] = ""

            # redirect and show toast in app.py
            st.session_state["tab"] = "Home"
            st.session_state["show_login_toast"] = True
            st.rerun()
        else:
            st.error(msg)

if __name__ == "__main__":
    main()
