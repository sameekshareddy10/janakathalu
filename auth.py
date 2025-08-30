import requests
import streamlit as st

API_BASE = "https://api.corpus.swecha.org/api/v1"

def login(phone: str, password: str):
    """Login and store token in session_state"""
    url = f"{API_BASE}/auth/login"
    payload = {"phone": phone, "password": password}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            st.session_state["access_token"] = data["access_token"]  # Store token in session
            st.session_state["token_type"] = data["token_type"]  # Store token type if needed
            return True, "Login successful ✅"
        elif response.status_code == 422:
            return False, "Validation error ❌ (Check phone/password format)"
        else:
            return False, f"Login failed ❌ ({response.status_code}) - {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_current_user():
    """Fetch user details using stored token"""
    if "access_token" not in st.session_state:
        return None

    url = f"{API_BASE}/auth/me"
    headers = {
        "Authorization": f"Bearer {st.session_state['access_token']}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def logout():
    """Clear session"""
    st.session_state.pop("access_token", None)
    st.session_state.pop("token_type", None)
    st.session_state.pop("user", None)
    st.session_state.pop("name", None)
