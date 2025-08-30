import streamlit as st
from utils.story_gen import chat_with_ai
from utils.save_data import (
    save_chat,
    save_chat_message,
    load_user_chat_history,
    clear_user_chat_history,
    load_data
)

st.set_page_config(page_title="Janasaarthi - Chat Assistant", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
        .sticky-top {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            z-index: 9999;
            padding: 20px 30px 10px 30px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        .chat-box {
            margin-top: 130px;
            height: 450px;
            overflow-y: auto;
            padding: 10px 30px;
        }
        .input-form {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 10px 30px;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            z-index: 9998;
        }
        input[type="text"] {
            autocomplete: off !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Init Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state["user"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "last_loaded_user" not in st.session_state:
    st.session_state["last_loaded_user"] = None
if "chat_input" not in st.session_state:  
    st.session_state.chat_input = ""
if "reset_input" not in st.session_state:
    st.session_state.reset_input = False

username = st.session_state.get("user", None)

# --- Sticky Top Bar ---
st.markdown('<div class="sticky-top">', unsafe_allow_html=True)

st.markdown("## 🌐 Choose your language:")
language = st.selectbox(
    "Choose a language",
    ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Bengali", "Malayalam"],
    key="language_selector",
    label_visibility="collapsed"
)

# 🧹 Clear button (only for logged-in users)
if username:
    if st.button("🗑️ Clear My Chat History"):
        clear_user_chat_history(username)
        st.session_state.messages = []
        st.session_state.chat_input = ""
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# --- Load chat history only for logged-in user ---
if username and st.session_state["last_loaded_user"] != username:
    st.session_state.messages = []
    history = load_user_chat_history(username)
    for entry in history:
        if "role" in entry and "message" in entry:
            st.session_state.messages.append({
                "role": entry["role"],
                "content": entry["message"]
            })
    st.session_state["last_loaded_user"] = username

# --- Chat History Box ---
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if "role" in msg and "content" in msg:
        role = "🧍 You" if msg["role"] == "user" else "🧠 Janasaarthi"
        bg = "#d0e7ff" if msg["role"] == "user" else "#d6f5d6"
        color = "#003366" if msg["role"] == "user" else "#004d00"
        st.markdown(f"""
            <div style="background-color: {bg}; color: {color}; padding: 10px;
                        border-radius: 10px; margin: 5px 0; max-width: 75%;">
                <b>{role}:</b> {msg["content"]}
            </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Reset chat input before rendering widget ---
if st.session_state.get("reset_input", False):
    st.session_state["chat_input"] = ""
    st.session_state["reset_input"] = False

# --- Input Form ---
with st.form(key="chat_form"):
    st.markdown('<div class="input-form">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([7, 1, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col2:
        send = st.form_submit_button("Send")
    with col3:
        clear = st.form_submit_button("Clear")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Handle Send ---
if send and st.session_state.chat_input.strip():
    message = st.session_state.chat_input.strip()
    st.session_state.messages.append({"role": "user", "content": message})
    with st.spinner("Janasaarthi is thinking..."):
        reply = chat_with_ai(message, st.session_state.language_selector)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    if username:
        save_chat_message(username, "user", message)
        save_chat_message(username, "assistant", reply)
        save_chat(message, reply, st.session_state.language_selector, username)

    st.session_state.reset_input = True
    st.rerun()

# --- Handle Clear ---
if clear:
    st.session_state.messages = []
    st.session_state.reset_input = True
    st.rerun()

# --- Show only logged-in user's multilingual chat logs ---
if username:
    with st.expander("📜 View My Multilingual Chat Logs"):
        chat_logs = load_data("data/chat_logs_lang.json")
        user_logs = [log for log in chat_logs if log.get("username") == username]
        for chat in user_logs:
            if "user_message" in chat and "assistant_reply" in chat:
                st.markdown(f"""
                - 🧍 **You:** {chat["user_message"]}
                - 🧠 **Janasaarthi:** {chat["assistant_reply"]}
                """)
