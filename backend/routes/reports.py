import os
import uuid
from flask import request, jsonify, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from fpdf import FPDF

from extensions import db
from models import Report
from schemas.reports import ReportSchema
from utils.text_extractor import extract_text_from_file
from utils.ai_manager import analyze_report

reports_blp = Blueprint(
    "reports", "reports", url_prefix="/api/reports", description="Operations on reports"
)

UPLOAD_FOLDER = "backend/static/uploads/reports"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@reports_blp.route("/summarize")
class ReportUpload(MethodView):
    @jwt_required()
    def post(self):
        """Upload a report for summarization"""
        senior_id = get_jwt_identity()
        if "file" not in request.files:
            abort(400, message="No file part in the request.")

        file = request.files["file"]

        if file.filename == "":
            abort(400, message="No selected file.")

        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            stored_filename = f"{uuid.uuid4().hex}_{original_filename}"
            filepath = os.path.join(UPLOAD_FOLDER, stored_filename)

            file.save(filepath)

            extracted_text = extract_text_from_file(filepath)
            summary = None
            if extracted_text:
                summary = analyze_report(extracted_text)
                status = "completed"
            else:
                status = "failed"

            new_report = Report(
                senior_id=senior_id,
                original_filename=original_filename,
                stored_filename=stored_filename,
                extracted_text=extracted_text,
                summary=summary,
                status=status,
            )
            db.session.add(new_report)
            db.session.commit()

            if status == "completed":
                return (
                    jsonify(
                        {
                            "message": "File processed successfully.",
                            "report": ReportSchema().dump(new_report),
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify({"message": "Failed to extract text from the file."}),
                    422,
                )

        else:
            abort(400, message="File type not allowed.")


@reports_blp.route("/<string:report_id>/download")
class ReportDownload(MethodView):
    @jwt_required()
    def get(self, report_id):
        """Download the summary of a report as a PDF"""
        report = Report.query.get_or_404(report_id)

        if not report.summary:
            abort(404, message="Summary not available for this report.")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add a title
        pdf.cell(200, 10, txt="AI Report Analysis", ln=True, align="C")
        pdf.ln(10)

        # Add the summary text
        # The text needs to be encoded properly to handle special characters
        summary_text = report.summary.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, txt=summary_text)

        # Create the PDF response
        pdf_output = pdf.output(dest="S").encode("latin-1")

        return Response(
            pdf_output,
            mimetype="application/pdf",
            headers={
                "Content-disposition": f"attachment; filename=summary_{report_id}.pdf"
            },
        )
