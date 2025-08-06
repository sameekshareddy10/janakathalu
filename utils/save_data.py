import os
import json
from datetime import datetime

# --- File Paths ---
CHAT_LOG_FILE = "data/chat_logs.json"            # for user messages
LANG_LOG_FILE = "data/chat_logs_lang.json"       # for multilingual logs

STORY_LOG_FILE = "data/story_submissions.json"

# ---------- Ensure file/folder exists ----------
def ensure_data_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f)

# ---------- Load JSON ----------
def load_data(filename):
    ensure_data_file(filename)
    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# ---------- Save generic data ----------
def save_submission(entry, filename):
    ensure_data_file(filename)
    data = load_data(filename)
    data.append(entry)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ========== CHAT ==========

# Save chat entry (multilingual/global)
def save_chat(user_input, assistant_reply, language, username=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "language": language,
        "user_message": user_input,
        "assistant_reply": assistant_reply,
    }
    if username:
        entry["username"] = username
    save_submission(entry, LANG_LOG_FILE)  # if you've renamed it; otherwise use CHAT_LOG_FILE

# Save per-message chat (user-specific)
def save_chat_message(username, role, message):
    """Save a user-specific chat message."""
    if not username:
        return  # Don't save guest messages
    entry = {
        "username": username,
        "role": role,
        "message": message
    }
    logs = load_data(CHAT_LOG_FILE)
    logs.append(entry)
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


# Load only messages from a given user
def load_user_chat_history(username):
    logs = load_data(CHAT_LOG_FILE)
    return [msg for msg in logs if msg.get("username") == username and "role" in msg and "message" in msg]

# Clear specific user's chat
def clear_user_chat_history(username):
    logs = load_data(CHAT_LOG_FILE)
    filtered = [msg for msg in logs if msg.get("username") != username]
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2)

# ========== STORY ==========

def rate_story(story_id, rating):
    stories = load_data(STORY_LOG_FILE)
    for story in stories:
        if story.get("id") == story_id:
            story.setdefault("ratings", []).append(rating)
            break
    with open(STORY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=4)

def comment_on_story(story_id, text):
    stories = load_data(STORY_LOG_FILE)
    for story in stories:
        if story.get("id") == story_id:
            story.setdefault("comments", []).append({
                "text": text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            break
    with open(STORY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=4)

def update_story(story_id, updated_data):
    stories = load_data(STORY_LOG_FILE)
    for i, story in enumerate(stories):
        if story.get("id") == story_id:
            stories[i].update(updated_data)
            break
    with open(STORY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=4)
