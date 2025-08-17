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
    description="This blueprint provides an AI-powered chat functionality that allows users to interact with their uploaded medical reports. Users can ask questions about a specific report, and the system will provide intelligent answers based on the report's content. This feature is designed to help users better understand complex medical information and get quick clarifications on their health data.",
)


@chat_blp.route("/<string:report_id>")
class Chat(MethodView):
    @jwt_required()
    @chat_blp.doc(
        summary="Chat with a specific medical report",
        description="This endpoint enables users to send a message to the chatbot for a specific medical report. By providing a report ID and a user question, the system leverages AI to analyze the report's content and generate a relevant, context-aware response. This interactive feature makes it easier for users to engage with their health documents and extract meaningful information.",
    )
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
