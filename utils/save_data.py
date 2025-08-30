import os
import json
from datetime import datetime

# --- File Paths ---
CHAT_LOG_FILE = "data/chat_logs.json"          # per-message user chat
LANG_LOG_FILE = "data/chat_logs_lang.json"     # multilingual chat logs
STORY_LOG_FILE = "data/story_submissions.json" # story submissions

# ---------- Helpers ----------
def _ensure_data_file(file_path):
    """Ensure the JSON file exists and is initialized as a list."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

def _load_json(file_path):
    """Safely load JSON data from file."""
    _ensure_data_file(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_json(file_path, data):
    """Save JSON data to file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------- Generic ----------
def load_data(file_path):
    """Load JSON from any file."""
    return _load_json(file_path)

def save_submission(submission, file_path):
    """Save a generic entry (e.g. story or chat)."""
    data = _load_json(file_path)
    if "timestamp" not in submission:
        submission["timestamp"] = datetime.now().isoformat()
    data.append(submission)
    _save_json(file_path, data)

# ========== CHAT ==========
def save_chat(user_input, assistant_reply, language, username=None):
    """Save multilingual/global chat log."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "language": language,
        "user_message": user_input,
        "assistant_reply": assistant_reply,
    }
    if username:
        entry["username"] = username
    save_submission(entry, LANG_LOG_FILE)

def save_chat_message(username, role, message):
    """Save a user-specific chat message (per message)."""
    if not username:
        return
    entry = {
        "username": username,
        "role": role,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    logs = _load_json(CHAT_LOG_FILE)
    logs.append(entry)
    _save_json(CHAT_LOG_FILE, logs)

def load_user_chat_history(username):
    """Load chat history only for one user."""
    logs = _load_json(CHAT_LOG_FILE)
    return [msg for msg in logs if msg.get("username") == username]

def clear_user_chat_history(username):
    """Clear a user's chat history from both normal and multilingual logs."""
    # Per-message logs
    logs = _load_json(CHAT_LOG_FILE)
    logs = [msg for msg in logs if msg.get("username") != username]
    _save_json(CHAT_LOG_FILE, logs)

    # Multilingual logs
    lang_logs = _load_json(LANG_LOG_FILE)
    lang_logs = [log for log in lang_logs if log.get("username") != username]
    _save_json(LANG_LOG_FILE, lang_logs)

# ========== STORY ==========
def rate_story(story_id, rating):
    """Add a rating to a story."""
    stories = _load_json(STORY_LOG_FILE)
    for story in stories:
        if story.get("id") == story_id:
            story.setdefault("ratings", []).append(rating)
            break
    _save_json(STORY_LOG_FILE, stories)

def comment_on_story(story_id, text):
    """Add a comment to a story."""
    stories = _load_json(STORY_LOG_FILE)
    for story in stories:
        if story.get("id") == story_id:
            story.setdefault("comments", []).append({
                "text": text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            break
    _save_json(STORY_LOG_FILE, stories)

def update_story(story_id, updated_data):
    """Update a story with new data."""
    stories = _load_json(STORY_LOG_FILE)
    for i, story in enumerate(stories):
        if story.get("id") == story_id:
            stories[i].update(updated_data)
            break
    _save_json(STORY_LOG_FILE, stories)
