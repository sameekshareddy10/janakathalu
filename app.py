import streamlit as st
from pathlib import Path
from PIL import Image
import base64


# ---------- Page config ----------
st.set_page_config(page_title="JanaKathalu", layout="wide")

# ---------- Session defaults ----------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "tab" not in st.session_state:
    st.session_state["tab"] = "Home"

# ---------- Navbar ---------
import streamlit as st
from pathlib import Path
import base64

def show_navbar():
    st.markdown("""
    <style>
    .navbar {
        background-color: #fff7ed;
        padding: 1rem 2rem;
        border-bottom: 3px solid #facc15;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .navbar h1 {
        color: #ea580c;
        font-size: 2rem;
        margin: 0;
    }
    .empty-profile {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e5e7eb;
        border: 2px solid #d1d5db;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 2])
    with cols[0]:
        st.markdown("<div class='navbar'><h1>📚 JanaKathalu</h1></div>", unsafe_allow_html=True)

    with cols[1]:
        buttons = ["🏠 Home", "📊 Dashboard", "👤 Profile"]
        tab_keys = ["Home", "Dashboard", "Profile"]
        if st.session_state["user"]:
            buttons.append("🚪 Logout")
            tab_keys.append("Logout")
        else:
            buttons.append("🔐 Login")
            tab_keys.append("Login")

        # User info
        username = st.session_state["user"] if st.session_state["user"] else "Guest"
        profile_pic_path = (
            Path("data/profile_pics") / f"{st.session_state['user']}.png"
            if st.session_state["user"]
            else None
        )

        profile_cols = st.columns([1, 4, 1])
        with profile_cols[1]:
            inner = st.columns([1, 6])  # tighter layout than [1, 4]
            with inner[0]:
                if profile_pic_path and profile_pic_path.exists():
                    with open(profile_pic_path, "rb") as f:
                        b64_img = base64.b64encode(f.read()).decode("utf-8")
                    st.markdown(
                        f"""
                        <div style="
                            width: 40px;
                            height: 40px;
                            border-radius: 50%;
                            overflow: hidden;
                            border: 2px solid #d1d5db;
                            background-color: #e5e7eb;
                        ">
                            <img src="data:image/png;base64,{b64_img}" 
                                 style="width: 100%; height: 100%; object-fit: cover;" />
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown("<div class='empty-profile'></div>", unsafe_allow_html=True)
            with inner[1]:
                st.markdown(f"<div style='font-size: 1rem;'><strong>{username}</strong></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        btn_cols = st.columns(len(buttons))
        for btn_label, btn_key, col in zip(buttons, tab_keys, btn_cols):
            with col:
                if st.button(btn_label, key=f"nav_{btn_key}"):
                    st.session_state["tab"] = btn_key
                    st.rerun()

show_navbar()

# ---------- Toast after login ----------
if st.session_state.get("show_login_toast"):
    st.toast("✅ Successfully Logged In!", icon="🎉")
    st.session_state["show_login_toast"] = False

# ---------- Page Content ----------
tab = st.session_state["tab"]

if tab == "Home":
    name = st.session_state["name"]
    st.title(f"📚 Welcome to JanaKathalu{f', {name}!' if name else '!'}")
    st.markdown("## ✨ Your Story, Your Voice\nJanaKathalu is a joyful space for everyone — grandparents, parents, children, and young creators — to **share, listen, and relive timeless tales**.")
    st.markdown("---")
    st.markdown("### 🌟 Explore Our Features")

    features = [
        {"name": "Text to Speech", "icon": "🗣️", "page": "text_to_speech"},
        {"name": "Speech to Text", "icon": "🎙️", "page": "speech_to_text"},
        {"name": "Story Generator", "icon": "📖", "page": "story_generator"},
        {"name": "Chat Assistant", "icon": "🤖", "page": "chat_assistant"},
        {"name": "Translator", "icon": "🌍", "page": "translator"},
    ]

    # Group into rows of 3
    rows = [features[i:i+3] for i in range(0, len(features), 3)]

    for row in rows:
        # Pad row if fewer than 3 items
        while len(row) < 3:
            row.append({"name": "", "icon": "", "page": ""})
        cols = st.columns(3)
        for col, feat in zip(cols, row):
            with col:
                if feat["name"]:  # Only render if not dummy
                    st.markdown("<div style='text-align:center; padding:10px;'>", unsafe_allow_html=True)
                    if st.button(f"{feat['icon']}  \n**{feat['name']}**", key=feat["name"]):
                        st.switch_page(f"pages/{feat['page']}.py")
                    st.markdown("</div>", unsafe_allow_html=True)

elif tab == "Dashboard":
    if st.session_state["user"]:
        st.title("📊 Dashboard")
        st.info("Here you will see your submissions, stats, and more!")
    else:
        st.warning("Login required.")
        st.session_state["tab"] = "Login"
        st.rerun()

elif tab == "Profile":
    if st.session_state["user"]:
        st.title("👤 Your Profile")
        st.write(f"**Username:** {st.session_state['user']}")
        st.write(f"**Name:** {st.session_state.get('name', '')}")

        profile_pic_path = Path("data/profile_pics") / f"{st.session_state['user']}.png"
        if profile_pic_path.exists():
            st.image(str(profile_pic_path), width=150)

        uploaded = st.file_uploader("Update Profile Picture", type=["png", "jpg", "jpeg"])
        if uploaded:
            Path("data/profile_pics").mkdir(parents=True, exist_ok=True)
            with open(profile_pic_path, "wb") as f:
                f.write(uploaded.read())
            st.success("Profile picture updated!")
            st.rerun()

        if st.button("🗑️ Delete My Account"):
            st.warning("Feature coming soon.")
    else:
        st.warning("Login required.")
        st.session_state["tab"] = "Login"
        st.rerun()

elif tab == "Login":
    st.switch_page("pages/login.py")


elif tab == "Logout":
    st.session_state.clear()
    st.toast("👋 Logged out", icon="🚪")
    st.session_state["tab"] = "Home"
    st.rerun() 