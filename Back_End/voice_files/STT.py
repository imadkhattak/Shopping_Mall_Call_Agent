from openai import OpenAI
from ..src.config import openai_api_key

client = OpenAI(api_key=openai_api_key)

def stt(audio_file):
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return response.text