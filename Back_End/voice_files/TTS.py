from openai import OpenAI
from ..src.config import openai_api_key

client = OpenAI(api_key=openai_api_key)

def tts(text):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy_female",
        input=text,
    )
    with open("audio.mp3", "wb") as f:
        f.write(response.content)