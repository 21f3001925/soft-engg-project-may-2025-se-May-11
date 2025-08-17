from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from models import Report
from utils.ai_manager import chat_with_report

chat_blp = Blueprint(
    "chat",
    "chat",
    url_prefix="/api/chat",
    description="Operations for the chat feature",
)


@chat_blp.route("/<string:report_id>")
class Chat(MethodView):
    @jwt_required()
    def post(self, report_id):
        """Send a message to the chatbot for a specific report."""
        json_data = request.get_json()
        user_question = json_data.get("message")

        if not user_question:
            abort(400, message="'message' is a required field.")

        report = Report.query.get_or_404(report_id)

        if not report.extracted_text:
            abort(
                422,
                message="Cannot chat about this report as its text could not be extracted.",
            )

        ai_response = chat_with_report(report.extracted_text, user_question)

        return jsonify({"response": ai_response}), 200
