from datetime import datetime, timezone
from google.cloud import texttospeech
from google.cloud import speech

from utils.ai_manager import get_query_intent
from models import Appointment, Medication, EmergencyContact

# Configure Google Cloud TTS and STT Clients
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
try:
    tts_client = texttospeech.TextToSpeechClient()
    stt_client = speech.SpeechClient()
except Exception as e:
    print(f"Error configuring Google Cloud clients: {e}")
    tts_client = None
    stt_client = None


def process_voice_query(audio_content: bytes, user_id: str) -> bytes:
    """Processes a voice query (audio), gets intent, fetches data, and returns audio."""

    if not stt_client:
        return b""  # STT client not configured

    # 1. Convert audio to text using Google Cloud STT
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Assuming 16kHz, adjust if needed
        language_code="en-US",
    )

    try:
        stt_response = stt_client.recognize(config=config, audio=audio)
        if not stt_response.results:
            return _generate_tts_audio("I didn't catch that. Could you please repeat?")
        query_text = stt_response.results[0].alternatives[0].transcript
        print(f"STT recognized: {query_text}")
    except Exception as e:
        print(f"Error during STT: {e}")
        return _generate_tts_audio(
            "I had trouble understanding your voice. Please try again."
        )

    # 2. Get intent from LLM
    intent_data = get_query_intent(query_text)
    intent = intent_data.get("intent", "unknown")

    response_text = ""

    if intent == "get_next_appointment":
        now = datetime.now(timezone.utc)
        next_appointment = (
            Appointment.query.filter(
                Appointment.senior_id == user_id, Appointment.date_time > now
            )
            .order_by(Appointment.date_time.asc())
            .first()
        )

        if next_appointment:
            date_str = next_appointment.date_time.strftime("%A, %B %d at %I:%M %p")
            response_text = (
                f"Your next appointment is on {date_str} with {next_appointment.title}."
            )
        else:
            response_text = "You have no upcoming appointments."

    elif intent == "get_medication_schedule":
        now = datetime.now(timezone.utc)
        next_medication = (
            Medication.query.filter(
                Medication.senior_id == user_id, Medication.time > now
            )
            .order_by(Medication.time.asc())
            .first()
        )

        if next_medication:
            time_str = next_medication.time.strftime("%I:%M %p")
            response_text = f"You need to take {next_medication.name} at {time_str}."
        else:
            response_text = "You have no upcoming medications scheduled."

    elif intent == "get_emergency_contacts":
        contacts = EmergencyContact.query.filter_by(senior_id=user_id).all()
        if contacts:
            contact_list = ", ".join([c.name for c in contacts])
            response_text = f"Your emergency contacts are: {contact_list}."
        else:
            response_text = "You have not added any emergency contacts yet."

    else:  # unknown intent
        response_text = "I'm sorry, I don't understand that request. Please try asking about appointments or medications."

    # 3. Convert text response to audio using Google Cloud TTS
    return _generate_tts_audio(response_text)


def _generate_tts_audio(text: str) -> bytes:
    """Helper function to generate TTS audio using Google Cloud TTS."""
    if not tts_client:
        return b""  # Return empty bytes if TTS client not configured

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # A high-quality voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        tts_response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return tts_response.audio_content
    except Exception as e:
        print(f"Error during TTS: {e}")
        return b""
