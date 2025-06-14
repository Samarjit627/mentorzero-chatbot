# MentorZero YC Chatbot

MentorZero is a Streamlit-based chatbot that channels the persona of a YC partner to give direct, practical, and context-grounded advice to founders. It features persistent chat history, dynamic chat UI, and supports both RAG (retrieval-augmented generation) and OpenAI completions.

## Features
- Dynamic, modern chat UI (WhatsApp/ChatGPT style)
- Persistent chat history and conversation management
- Source attribution for retrieved knowledge
- Displays token usage, API cost, and response time
- Light and dark mode support (customizable)
- Easily deployable to Replit, Streamlit Cloud, or locally

## Requirements
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage
1. **Add your OpenAI API key:**
   - Set the `OPENAI_API_KEY` environment variable, or edit `chatbot_app.py` to set it directly.
2. **Run the app:**
   ```sh
   streamlit run chatbot_app.py
   ```
3. **Open your browser:**
   - Go to `http://localhost:8501` (or the port shown in your terminal)

## Deploy to Replit
- Push this repo to GitHub
- Import into Replit
- Set the run command to:
  ```sh
  streamlit run chatbot_app.py --server.port=8080 --server.address=0.0.0.0
  ```
- Add your OpenAI API key as a secret in Replit

## Project Structure
```
.
├── chatbot_app.py           # Main Streamlit app
├── chatbot_style.css        # Custom chat UI styles (dark)
├── chatbot_style_light.css  # Custom chat UI styles (light)
├── rag_logic.py             # Retrieval-augmented generation logic
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── ...                      # Data and other modules
```

## License
This project is for educational and prototyping purposes. Please check OpenAI's terms for API usage.

---

*Built by Samarjit, powered by Streamlit and OpenAI.*
