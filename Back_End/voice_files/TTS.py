from elevenlabs.client import ElevenLabs
from ..src.config import elevenlabs_api_key

client = ElevenLabs(api_key=elevenlabs_api_key)


def tts(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Change if you want another voice
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Save audio file
    with open("audio.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)