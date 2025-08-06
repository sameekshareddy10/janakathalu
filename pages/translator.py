import streamlit as st
from utils.translation import translate_text, LANG_MAP

st.title("Janasaarthi: Multilingual Translation")

source_lang = st.selectbox("Source Language (Optional - auto detect if none)", ["Auto Detect"] + list(LANG_MAP.keys()))
target_lang = st.selectbox("Target Language", list(LANG_MAP.keys()))
text = st.text_area("Enter text to translate")

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        source = None if source_lang == "Auto Detect" else source_lang
        translated_text = translate_text(text, target_lang, source)
        st.subheader("Translated Text:")
        st.write(translated_text)
