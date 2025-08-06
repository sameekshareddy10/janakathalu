import json
import os
import hashlib

USER_DATA_FILE = "data/users.json"

# ---------- Ensure the file exists ----------
def ensure_user_file():
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

# ---------- Load users ----------
def load_users():
    ensure_user_file()
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# ---------- Save users ----------
def save_users(users):
    ensure_user_file()
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

# ---------- Hash password ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- Register user ----------
def register_user(username, name, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "name": name,
        "password": hash_password(password)
    }
    save_users(users)
    return True, "Registration successful!"

# ---------- Login user ----------
def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found.", None
    hashed = hash_password(password)
    if users[username]["password"] != hashed:
        return False, "Incorrect password.", None
    return True, "Login successful!", users[username]["name"]
