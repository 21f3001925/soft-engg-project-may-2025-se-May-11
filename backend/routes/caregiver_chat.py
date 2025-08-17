from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from utils.caregiver_chat_manager import process_caregiver_query

caregiver_chat_blp = Blueprint(
    "caregiver_chat",
    "caregiver_chat",
    url_prefix="/api/caregiver-chat",
    description="Operations for caregiver chat",
)


@caregiver_chat_blp.route("/<string:senior_id>")
class CaregiverChat(MethodView):
    @jwt_required()
    def post(self, senior_id):
        """Send a message to the caregiver chatbot for a specific senior."""
        json_data = request.get_json()
        query_text = json_data.get("message")

        if not query_text:
            abort(400, message="'message' is a required field.")

        response_text = process_caregiver_query(query_text, senior_id)

        return jsonify({"response": response_text}), 200
