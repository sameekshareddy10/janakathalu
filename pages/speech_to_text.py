import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile

# Supported languages and codes
LANG_MAP = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "Kannada": "kn", "Bengali": "bn", "Marathi": "mr",
    "Gujarati": "gu", "Malayalam": "ml", "Punjabi": "pa"
}

st.set_page_config(page_title="Speech to Text Translator", layout="centered")
st.title("🎤 Speech to Text & Translate")

# Language selection
source_lang_name = st.selectbox("🎙️ Spoken Language", list(LANG_MAP.keys()), index=0)
target_lang_name = st.selectbox("🌐 Translate To", list(LANG_MAP.keys()), index=1)

source_lang_code = LANG_MAP[source_lang_name]
target_lang_code = LANG_MAP[target_lang_name]

if st.button("🔴 Record and Translate"):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            # Create a placeholder for messages
            status_message = st.empty()
            
            # Show "Speak now" message
            status_message.info("🎙️ Speak now...")
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Replace "Speak now" with "Audio captured" message
            status_message.success("✅ Audio captured. Transcribing...")

        # Recognize speech
        try:
            text = recognizer.recognize_google(audio, language=source_lang_code)
            
            # Clear status message once transcription is ready
            status_message.empty()

            st.text_area("📝 Transcribed Text:", text, height=100)

            # Translate if needed
            if source_lang_code != target_lang_code:
                translated_text = GoogleTranslator(source=source_lang_code, target=target_lang_code).translate(text)
                st.text_area("🌐 Translated Text:", translated_text, height=100)
            else:
                translated_text = text

        except sr.UnknownValueError:
            status_message.empty()
            st.warning("😕 Sorry, we couldn't understand your speech. Please try again.")
        except sr.RequestError as e:
            status_message.empty()
            st.error(f"❌ Could not request results; check your internet connection.\n{e}")
        except Exception as e:
            status_message.empty()
            st.error(f"Unexpected error: {e}")

    except Exception as e:
        st.error(f"🎤 Microphone error or timeout: {e}")
