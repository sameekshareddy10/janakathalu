from deep_translator import GoogleTranslator

# Supported Indic and English languages
LANG_MAP = {
    "english": "en",
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "kannada": "kn",
    "bengali": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "malayalam": "ml",
    "punjabi": "pa"
}

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """
    Translate `text` to `target_language`.
    Optionally specify `source_language` or let it auto-detect.
    """
    target_lang_code = LANG_MAP.get(target_language.lower())
    if not target_lang_code:
        return f"Error: Unsupported target language '{target_language}'. Supported: {list(LANG_MAP.keys())}"
    
    try:
        if source_language:
            source_lang_code = LANG_MAP.get(source_language.lower())
            if not source_lang_code:
                return f"Error: Unsupported source language '{source_language}'. Supported: {list(LANG_MAP.keys())}"
            translator = GoogleTranslator(source=source_lang_code, target=target_lang_code)
        else:
            translator = GoogleTranslator(target=target_lang_code)  # autodetect source
        return translator.translate(text)
    except Exception as e:
        return f"Translation error: {e}"
