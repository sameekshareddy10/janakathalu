import streamlit as st
from huggingface_hub import InferenceClient

# Load API key from secrets
API_KEY = st.secrets["API_KEY"]

# Initialize the inference clients
story_client = InferenceClient(
    model="deepseek-ai/DeepSeek-V3-0324",
    token=API_KEY
)

chat_client = InferenceClient(
    model="deepseek-ai/DeepSeek-V3-0324",
    token=API_KEY
)

# ----------- Story Generator -------------
def generate_story(prompt, genre, language, word_limit):
    if word_limit.startswith("<"):
        approx_words = word_limit.replace("<", "").strip()
    else:
        approx_words = word_limit

    if not prompt.strip():
        prompt = f"Generate an imaginative story based on the {genre} genre."

    system_msg = (
        f"You are a creative story writer. Write a {genre} story in {language}. "
        f"The story should be around {approx_words} words long and engaging for the reader."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]

    try:
        response = story_client.chat.completions.create(
            messages=messages,
            temperature=0.7,
            max_tokens=1200 if int(approx_words) > 500 else 600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating story: {e}"

# ----------- Chat Assistant -------------
def chat_with_ai(user_input, language):
    messages = [
        {"role": "system", "content": f"You are Janasaarthi. You are a helpful assistant. Respond in {language}."},
        {"role": "user", "content": user_input}
    ]
    try:
        response = chat_client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error during chat: {e}"
