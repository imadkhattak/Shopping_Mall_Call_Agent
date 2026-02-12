# Back_End/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
import os

from .voice_files.STT import stt        # Your STT function
from .voice_files.TTS import tts        # Your OpenAI TTS function
from .src.agent_executor import agent_executor  # Your LangChain agent

app = FastAPI(title="Shopping Mall Voice Agent")

# -------------------------------
# Paths for frontend files
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Front_End")

app.mount("/styles", StaticFiles(directory=os.path.join(FRONTEND_DIR, "styles")), name="styles")
app.mount("/script", StaticFiles(directory=os.path.join(FRONTEND_DIR, "script")), name="script")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
async def read_root(request: Request):
    """
    Serve the frontend page
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start_conversation")
async def start_conversation():
    """
    Initial greeting
    """
    greeting_text = "Welcome to the shopping mall. How can I help you today?"
    tts(greeting_text)  # Generate audio
    return FileResponse("audio.mp3", media_type="audio/mpeg", filename="welcome.mp3")

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Handle user voice input with full debug logging:
    1. Save audio file
    2. STT to get text
    3. Send text to agent
    4. Extract AI message
    5. Convert to TTS
    6. Return audio
    """
    temp_filename = "temp_input.wav"

    print("=== START PROCESS AUDIO ===")
    print(f"Received file: {file.filename}")

    try:
        # Save uploaded file
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Saved temporary audio file: {temp_filename}")

        # -------------------------------
        # Speech-to-Text
        # -------------------------------
        with open(temp_filename, "rb") as audio_file:
            user_text = stt(audio_file)
        print(f"[DEBUG] STT output: {user_text}")

        if not user_text:
            print("[DEBUG] No speech detected in the audio")
            return {"error": "No speech detected"}

        # -------------------------------
        # Agent Response
        # -------------------------------
        print("[DEBUG] Sending text to agent_executor...")
        response = agent_executor.invoke({"messages": [{"role": "user", "content": user_text}]})
        print(f"[DEBUG] Raw agent response: {response}")

        messages = response["messages"] if isinstance(response, dict) else response.messages
        print("[DEBUG] Parsed agent messages:")
        for i, msg in enumerate(messages):
            print(f"  Message {i}: type={getattr(msg,'type',None)}, content={getattr(msg,'content',None)}")

        # -------------------------------
        # Extract AI message
        # -------------------------------
        final_message = None
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai":
                final_message = getattr(msg, "content", None)
                break

        if not final_message:
            final_message = "I'm sorry, I couldn't process that request."

        print(f"[DEBUG] Final agent message: {final_message}")

        # -------------------------------
        # Text-to-Speech
        # -------------------------------
        print("[DEBUG] Converting agent response to audio using TTS...")
        tts(final_message)  # Generates "audio.mp3"
        print("[DEBUG] TTS audio generated: audio.mp3")

        return FileResponse("audio.mp3", media_type="audio/mpeg", filename="response.mp3")

    except Exception as e:
        print(f"[ERROR] Exception during process_audio: {e}")
        return {"error": str(e)}

    finally:
        # Cleanup temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print(f"[DEBUG] Temporary file deleted: {temp_filename}")

        print("=== END PROCESS AUDIO ===")

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Back_End.main:app", host="0.0.0.0", port=8000, reload=True)
