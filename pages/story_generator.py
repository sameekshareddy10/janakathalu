import streamlit as st
from utils.story_gen import generate_story
from utils.save_data import save_submission

st.set_page_config(layout="wide")
st.title("📖 Janasaarthi - Story Generator")

# SESSION STATE
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "last_genres" not in st.session_state:
    st.session_state.last_genres = []
if "last_story" not in st.session_state:
    st.session_state.last_story = ""
if "reroll" not in st.session_state:
    st.session_state.reroll = False

# --- INPUT: Story Idea ---
prompt = st.text_area("🧠 Enter your story idea", height=120)

# --- GENRES ---
all_genres = [
    "Fairy Tales", "Folklore & Fables", "Adventure", "Animal Stories",
    "Fantasy", "Educational", "Humor", "Bedtime Stories",
    "Young Adult (YA) Romance", "Coming-of-Age", "Dystopian", "Urban Fantasy",
    "Science Fiction", "Mystery/Thriller", "Social Issues", "Paranormal",
    "Horror", "Romance", "Thriller", "Historical Fiction", "Contemporary Drama",
    "Satire", "Crime", "Psychological Fiction", "Family Sagas", "Cozy Mystery",
    "Inspirational", "Heartwarming", "Memoir/Biography", "Reflective/Literary Fiction",
    "Spiritual/Philosophical", "Gentle Romance", "Nostalgic Fiction"
]

selected_genres = st.multiselect(
    "🎭 Genre (searchable)", all_genres, key="all_genres"
)

# --- LANGUAGE ---
language = st.selectbox("🌐 Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Bengali", "Malayalam"])

# --- WORD COUNT (Custom only) ---
st.markdown("✍️ **Choose a story length (word count):**")

# Manual input for word count
word_limit = st.number_input(
    "Word count:", min_value=50, max_value=20000, step=50, key="manual"
)

word_limit = str(word_limit)


# --- BUTTONS: Generate & New Story ---
col1, col2 = st.columns([1, 1])
generate_clicked = False

with col1:
    if st.button("✨ Generate Story"):
        generate_clicked = True
        st.session_state.reroll = False

with col2:
    if st.button("🔄 Generate New Story"):
        generate_clicked = True
        st.session_state.reroll = True

# --- GENERATE STORY LOGIC ---
if generate_clicked:
    if not selected_genres:
        st.warning("Please select at least one genre.")
    else:
        genre_string = ", ".join(selected_genres)

        reuse_story = (
            prompt.strip() == st.session_state.last_prompt.strip() and
            selected_genres == st.session_state.last_genres and
            not st.session_state.reroll
        )

        if reuse_story and st.session_state.last_story:
            story = st.session_state.last_story
        else:
            with st.spinner("Janasaarthi is crafting your story..."):
                story = generate_story(prompt, genre_string, language, word_limit)
            st.session_state.last_prompt = prompt
            st.session_state.last_genres = selected_genres
            st.session_state.last_story = story
            st.session_state.reroll = False

        st.subheader("📘 Your Story:")
        st.write(story)
        from datetime import datetime

        entry = {
            "prompt": prompt,
            "genres": genre_string,
            "language": language,
            "word_limit": word_limit,
            "story": story,
            "username": st.session_state.get("user", "guest"),
            "timestamp": datetime.now().isoformat()
        }
        save_submission(entry, "data/story_submissions.json")
