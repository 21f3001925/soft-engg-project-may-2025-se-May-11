from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.voice_assistant_manager import process_voice_query

voice_blp = Blueprint(
    "voice",
    "voice",
    url_prefix="/api/voice-assistant",
    description="Operations for the voice assistant",
)


@voice_blp.route("/query")
class VoiceQuery(MethodView):
    @jwt_required()
    def post(self):
        """Receives audio query, processes it, and returns voice audio."""
        audio_content = request.data  # Get raw audio data

        if not audio_content:
            abort(400, message="No audio data provided.")

        user_id = get_jwt_identity()

        audio_data = process_voice_query(audio_content, user_id)

        if audio_data is None:
            abort(500, message="Failed to generate audio response.")

        return Response(audio_data, mimetype="audio/mpeg")

    def options(self):
        """Handles CORS preflight requests."""
        return "", 200
