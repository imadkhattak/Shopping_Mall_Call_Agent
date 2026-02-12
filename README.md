# Shopping Mall Voice Agent

A sophisticated, voice-activated AI assistant designed for shopping mall inquiries. This project leverages OpenAI for speech processing and LangChain for intelligent database interactions, wrapped in a modern, dark-themed web interface inspired by "Smith.ai".

## Features

- **Voice-Activated Interface**: Speak naturally to the agent without typing.
- **Intelligent Database Querying**: The agent understands natural language questions and executes SQL queries to fetch real-time mall data (stores, locations, etc.).
- **Silence Detection (VAD)**: Automatically detects when you stop speaking (1.5s threshold) and processes your request—no manual "stop" button needed.
- **Audio Feedback**: Responds with clear, human-like voice audio using OpenAI's TTS.
- **Modern UI**: A sleek, responsive dark-themed interface built with Vanilla JS and CSS.

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI & NLP**:
  - **STT (Speech-to-Text)**: OpenAI Whisper
  - **TTS (Text-to-Speech)**: OpenAI TTS (`tts-1-hd`)
  - **Agent Logic**: LangChain (SQL Database Toolkit)
  - **LLM**: OpenAI GPT-4 (via LangChain)
- **Database**: SQL (PostgreSQL/MySQL/SQLite depending on your config)

## Prerequisites

- Python 3.10+
- `uv` or `pip` for package management
- OpenAI API Key

## Setup & Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/imadkhattak/Shopping_Mall_Call_Agent.git
    cd Shopping_Mall_Call_Agent
    ```

2.  **Set Up Virtual Environment**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    # OR if using uv
    uv pip install -r requirements.txt
    ```

4.  **Environment Configuration**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    OPENAI_API_KEY=sk-your_api_key_here
    # Add other database credentials as needed by src/config.py
    ```

## Running the Application

1.  **Start the Backend Server**
    Run the following command from the project root:

    ```bash
    python -m uvicorn Back_End.main:app --host 0.0.0.0 --port 8000 --reload
    ```

    _Note: Ensure you are in the root directory `Shopping_Mall_Call_Agent`._

2.  **Access the Interface**
    Open your web browser and go to:
    [http://localhost:8000](http://localhost:8000)

## How to Use

1.  Click the **"Start Conversation"** button on the homepage.
2.  Grant microphone permissions if prompted.
3.  Speak your question clearly (e.g., "Where is the Nike store?" or "What restaurants are on the second floor?").
4.  Stop speaking. The system will automatically detect silence, process your request, and respond with voice audio.

## Project Structure

```
Shopping_Mall_Call_Agent/
├── Back_End/
│   ├── main.py                 # FastAPI application entry point
│   ├── src/                    # Core agent logic and configurations
│   ├── voice_files/            # STT and TTS helper modules
│   └── temp_input.wav          # Temporary audio storage
├── Front_End/
│   ├── templates/              # HTML files
│   ├── styles/                 # CSS stylesheets
│   └── script/                 # JavaScript files (VAD logic)
├── Data/                       # Database files or scripts
└── requirements.txt            # Python dependencies
```

## Troubleshooting

- **Microphone Issues**: Ensure your browser has permission to access the microphone.
- **Audio Not Playing**: Check if your system volume is up and the browser tab is not muted.
- **"No Module Named..."**: Ensure you have activated the virtual environment and installed all dependencies.
- **API Errors**: Verify your `OPENAI_API_KEY` in the `.env` file.
