# JanaKathalu – Voice/text Collection App

JanaKathalu is an open-source Streamlit-based application built during the Summer of AI 2025 Internship. It allows users to submit short stories or folk tales through voice or text. The stories are automatically transcribed, summarized, and saved for contributing to Telugu language AI datasets.

---

##  Features

- 🎙️ Voice-to-text conversion using SpeechRecognition and PyDub
- 📖 AI-based story summarization (OpenAI API)
- 🌐 Translation to English using Googletrans
- 💾 Saves stories in a simple text file or JSON
- 🖼️ Optional logo and audio upload support
- 🔐 API key management via .env file

---

## 🛠️ Tech Stack

- Streamlit
- Python
- OpenAI API
- SpeechRecognition
- PyDub
- Googletrans
- python-dotenv
- GitLab (code.swecha.org)

---

## 📁 Project Structure

```

JanaKathalu/
├── .streamlit/
│   └── config.toml             # Streamlit app settings
├── app.py                      # Main Streamlit app
├── pages/
│   ├── About.py                # About page
│   └── Explore_Stories.py      # Explore past stories
├── utils/
│   ├── whisper_utils.py        # Speech-to-text (Whisper)
│   ├── translation_utils.py    # Translate + summarize
│   ├── storage_utils.py        # Save to file/cloud
│   ├── tagging_utils.py        # Auto-tags/themes
│   └── language_utils.py       # Language detect, clean
├── data/
│   ├── raw/                    # Raw audio/text input
│   └── processed/              # Cleaned story data
├── assets/
│   ├── images/                 # Logos, UI images
│   └── audio_samples/          # Sample voice files
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
└── .gitignore                  # Ignore unnecessary files

---

## 👥 Team Members

- Shiva Kumar – shivakumar1
- Asma begum  – AsmaBegum7
- Sameeksha   - Sameeksha10
- Srujana     - Srujana.V
- Yashonandan - Yash2006

---

## 🎯 Objective

This project supports the creation of a Telugu corpus by making it easy for users to contribute regional stories. The collected content can later be used in training open-source language models focused on Indian culture and languages.

---

## 📄 Availability

This project is open-source.

---

## 🙏 Acknowledgements

We would like to express our heartfelt thanks to the following:

- *Swecha GitLab* – for providing a free and open-source development environment.
- *Streamlit* – for making it easy to build and share beautiful web apps with Python.
- *OpenAI Whisper* – for enabling powerful speech-to-text capabilities.
- *Google Translate API & Hugging Face Transformers* – for language translation and tagging.
- *Our Mentors and Faculty* – for their guidance and encouragement throughout the project.
- *The Open Source Community* – for documentation, support, and inspiration.

This project is a small contribution to the larger vision of open knowledge and storytelling.

## 🔗 Useful Links

- Project Repo: https://code.swecha.org/shivakumar1/janakathalu 
- Internship: Summer of AI 2025 – Viswam.AI & Swecha  
