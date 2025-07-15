import requests
from pydub import AudioSegment
from io import BytesIO
import os
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Secure way
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")    # or any voice ID available in your ElevenLabs account


def generate_voice(text, filename):
    url = "https://elevenlabs.io/app/voice-library?voiceId=tnSpp4vdxKPjI9w0GnoV"
    headers = {
        "xi-api-key": "sk_f35460d35e07586a0a1ac26a5b3b9938c7a0688259f72dd0",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        print("❌ ElevenLabs Error:", response.status_code)
        print("❌ Response content:", response.text)
        raise Exception("Failed to get audio from ElevenLabs")

    try:
        audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
        audio.export(filename, format="mp3")
        print("✅ Audio saved to", filename)
    except Exception as e:
        print("❌ Pydub decoding failed")
        print("Response content (first 100 chars):", response.content[:100])
        raise e
    if "audio/mpeg" not in response.headers.get("Content-Type", ""):
        print("❌ ElevenLabs API did NOT return audio!")
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Response (first 500):", response.text[:500])
        raise Exception("ElevenLabs API did not return audio/mpeg content")