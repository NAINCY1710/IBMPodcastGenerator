# 🎙️ AI Podcast Generator

A simple web app to create podcast scripts and generate voiceovers with the help of IBM Watson AI services

---

## 🚀 Features

- 📝 Generate podcast scripts using Watsonx's Granite Foundation Model
- 🎧 Convert scripts into human-like voiceovers using IBM Watson Text-to-Speech
- ⚡ Minimalistic responsive web interface built with Streamlit
- 🌐 Choose from multiple regional and expressive voices

---

## 🧠 Powered By

- **IBM Watsonx AI** for generating creative and concise podcast scripts
- **IBM Watson TTS** for synthesizing high-quality voiceovers
- **Streamlit** for an interactive and intuitive frontend

---

## 💻 Setup

```bash
git clone https://github.com/NAINCY1710/IBMPodcastGenerator.git
cd IBMPodcastGenerator
python -m venv venv
venv\Scripts\activate         # for Windows
source venv/bin/activate      # for Linux/macOS
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Configuration
Before running the app, add your IBM credentials to **`.streamlit/secrets.toml`**
```bash
[api_keys]
WATSONX_API_KEY = "your_watsonx_api_key"
IBM_PROJECT_ID = "your_ibm_project_id"
IBM_WATSON_TTS_API_KEY = "your_text_to_speech_api_key"
IBM_WATSON_TTS_URL = "your_text_to_speech_url"
```

---

## 👨‍💻 Contributors

- [Naincy Jain](https://www.linkedin.com/in/naincy-jain-38a20a283)
- [Aarjav Jain](https://www.linkedin.com/in/bharatwalejain)