import requests
import streamlit as st
import uuid
import json
import os

API_BASE = "https://api.corpus.swecha.org/api/v1"

# ------------------------------
# Local storage configuration
# ------------------------------
LOCAL_DIR = "local_stories"
os.makedirs(LOCAL_DIR, exist_ok=True)

# ------------------------------
# Authentication Check
# ------------------------------
def is_logged_in():
    return "access_token" in st.session_state

# ------------------------------
# Story Submission Feature
# ------------------------------
def story_submission():
    st.title("📖 Write & Submit Your Story")

    # Check if the user is logged in
    if not is_logged_in():
        st.warning("🚨 Please log in first.")
        return

    # --- Story Metadata ---
    title = st.text_input("Story Title")
    genres = [
        "Fairy Tales", "Folklore & Fables", "Adventure", "Animal Stories",
        "Fantasy", "Educational", "Humor", "Bedtime Stories",
        "Young Adult (YA) Romance", "Coming-of-Age", "Dystopian", "Urban Fantasy",
        "Science Fiction", "Mystery/Thriller", "Social Issues", "Paranormal",
        "Horror", "Romance", "Thriller", "Historical Fiction", "Contemporary Drama",
        "Satire", "Crime", "Psychological Fiction", "Family Sagas", "Cozy Mystery",
        "Inspirational", "Heartwarming", "Memoir/Biography", "Reflective/Literary Fiction",
        "Spiritual/Philosophical", "Gentle Romance", "Nostalgic Fiction"
    ]
    genre = st.selectbox("Select Genre", genres)

    # --- Chapters ---
    st.subheader("Chapters")
    if "chapters" not in st.session_state:
        st.session_state["chapters"] = []

    chapter_name = st.text_input("Chapter Name")
    chapter_content = st.text_area("Chapter Content")

    if st.button("➕ Add Chapter"):
        if chapter_name.strip() and chapter_content.strip():
            st.session_state["chapters"].append({
                "chapter": chapter_name.strip(),
                "content": chapter_content.strip()  # This is the chunk data
            })
            st.success(f"Chapter '{chapter_name}' added!")
        else:
            st.error("Please provide both chapter name and content.")

    # Display current chapters
    if st.session_state["chapters"]:
        st.markdown("### Current Chapters")
        for idx, ch in enumerate(st.session_state["chapters"], start=1):
            st.markdown(f"**{idx}. {ch['chapter']}**")
            st.write(ch["content"])

    # --- Submit Story ---
    if st.button("🚀 Submit Story"):
        if not title.strip():
            st.error("Story title is required!")
            return
        if not st.session_state["chapters"]:
            st.error("Please add at least one chapter!")
            return

        story_data = {
            "author": st.session_state["user"],   # phone number of logged-in user
            "name": st.session_state.get("name", ""),
            "title": title.strip(),
            "genre": genre,
            "chapters": st.session_state["chapters"]
        }

        # 1️⃣ Save locally first
        local_file = os.path.join(LOCAL_DIR, f"{title.strip().replace(' ','_')}.json")
        try:
            with open(local_file, "w", encoding="utf-8") as f:
                json.dump(story_data, f, ensure_ascii=False, indent=4)
            st.success(f"✅ Story saved locally: {local_file}")
        except Exception as e:
            st.error(f"Error saving locally: {e}")
            return

        # 2️⃣ Submit to Swecha Corpus using chunk upload
        try:
            api_url = f"{API_BASE}/records/upload/chunk"  # endpoint for chunk upload
            upload_uuid = str(uuid.uuid4())  # generate unique UUID for upload session
            total_chunks = len(story_data["chapters"])

            headers = {
                "Authorization": f"Bearer {st.session_state['access_token']}"
            }

            for index, chapter in enumerate(story_data["chapters"]):
                chunk_data = chapter["content"]  # This is the content of the chapter (your chunk data)
                chunk_filename = f"{title.strip().replace(' ','_')}_chapter_{index+1}.txt"  # Filename

                # Prepare the request payload for the chunk upload
                payload = {
                    'chunk': (chunk_filename, chunk_data.encode('utf-8')),  # Encode the content in UTF-8
                    'filename': chunk_filename,
                    'chunk_index': index + 1,  # Chunk index (e.g., 1 for the first chapter)
                    'total_chunks': total_chunks,  # Total number of chunks (e.g., 5)
                    'upload_uuid': upload_uuid  # Upload UUID (same for all chunks in the upload)
                }

                # Log the payload for debugging purposes
                st.write(f"Payload for chapter {index+1}: {payload}")

                # Send the chunk to the API with authentication (headers with token)
                response = requests.post(api_url, files=payload, headers=headers)

                # Log the response for debugging purposes
                st.write(f"Response Status: {response.status_code}")
                st.write(f"Response Text: {response.text}")

                if response.status_code == 200:
                    st.success(f"✅ Chapter {index + 1} uploaded successfully!")
                else:
                    st.error(f"Error uploading chapter {index + 1}: {response.status_code} - {response.text}")
                    break  # Stop further uploads if an error occurs

            # If all chunks are uploaded successfully, finalize the upload
            if response.status_code == 200:
                finalize_upload(upload_uuid, title, total_chunks, chunk_filename, st.session_state["user"], genre, "english")
                st.session_state["chapters"] = []  # reset chapters
                st.experimental_rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"Network error while submitting to Corpus: {e}")

# Finalize the upload once all chunks are uploaded
def finalize_upload(upload_uuid, title, total_chunks, filename, user_id, category_id, language):
    api_url = f"{API_BASE}/records/upload"  # Finalize upload endpoint
    
    # Prepare the data for the finalization request
    data = {
        "title": title,
        "description": "Story submission",  # You can customize this if needed
        "category_id": category_id,
        "user_id": user_id,
        "media_type": "text",  # Assuming text format
        "upload_uuid": upload_uuid,
        "filename": filename,
        "total_chunks": total_chunks,
        "release_rights": "creator",  # Assuming creator rights
        "language": language,  # Language of the story
        "latitude": None,  # Optional, can be set if you have location data
        "longitude": None,  # Optional, can be set if you have location data
        "use_uid_filename": True  # Use UUID as the filename instead of the original filename
    }

    headers = {
        "Authorization": f"Bearer {st.session_state['access_token']}"  # Add the access token for authentication
    }

    # Send the POST request to finalize the upload with authentication
    try:
        response = requests.post(api_url, data=data, headers=headers)

        if response.status_code == 201:
            st.success("✅ Story uploaded and finalized successfully!")
            # The response will typically include metadata for the uploaded record (like its ID).
            response_data = response.json()  # Convert the response to JSON
            st.write(f"Record created with ID: {response_data.get('uid')}")
        else:
            st.error(f"Error finalizing upload: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error while finalizing upload: {e}")

# ------------------------------
# Run the feature
# ------------------------------
if __name__ == "__main__":
    story_submission()
