# backend/routes/voice.py
from flask import Blueprint, request, jsonify
from voice_utils import generate_voice

voice_blp = Blueprint("voice", __name__)

@voice_blp.route("/api/voice-appointment", methods=["POST"])
def voice_appointment():
    data = request.get_json()
    title = data.get("title")
    location = data.get("location")
    date_time = data.get("date_time")

    if not all([title, location, date_time]):
        return jsonify({"error": "Missing fields"}), 400

    text = f"You have an upcoming appointment. Title: {title}. Location: {location}. Date and Time: {date_time}."
    filename = f"{title.replace(' ', '_')}_reminder.mp3"

    try:
        audio_url = generate_voice(text, filename)
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
