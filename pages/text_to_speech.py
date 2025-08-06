import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile

# Language map (user-friendly to language codes)
LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

st.title("🔊 Text Translator & Speaker")

text = st.text_area("Enter text (in any language):")

target_lang_name = st.selectbox("Select language to translate and speak in:", list(LANG_MAP.keys()))
target_lang_code = LANG_MAP[target_lang_name]

if st.button("🔁 Translate & Speak"):
    if text.strip():
        try:
            # Translate text to selected language
            translated_text = GoogleTranslator(target=target_lang_code).translate(text)

            # Display translated text
            st.subheader("📝 Translated Text:")
            st.write(translated_text)

            # Convert to speech
            tts = gTTS(text=translated_text, lang=target_lang_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                audio_file = tmp_file.name

            # Play audio in Streamlit
            audio_bytes = open(audio_file, "rb").read()
            st.subheader("🔉 Listen:")
            st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"Error during translation or speech synthesis: {e}")
    else:
        st.warning("⚠️ Please enter some text to translate and speak.")
