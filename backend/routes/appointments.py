from flask import Blueprint, request, jsonify
from models import Appointment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

appointments_bp = Blueprint("appointments", __name__)

db = SQLAlchemy()


# Get all appointments
@appointments_bp.route("/appointments", methods=["GET"])
def get_appointments():
    appts = db.query(Appointment).all()
    return jsonify(
        [
            {
                "appointment_id": str(a.appointment_id),
                "title": a.title,
                "date_time": a.date_time.isoformat(),
                "location": a.location,
                "senior_id": str(a.senior_id),
            }
            for a in appts
        ]
    )


# Create appointment
@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()
    try:
        appt = Appointment(
            appointment_id=uuid.uuid4(),
            title=data["title"],
            date_time=datetime.fromisoformat(data["date_time"]),
            location=data["location"],
            senior_id=uuid.UUID(data["senior_id"]),
        )
        db.add(appt)
        db.commit()
        return (
            jsonify({"message": "Appointment created", "id": str(appt.appointment_id)}),
            201,
        )
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400


# Update appointment
@appointments_bp.route("/appointments/<uuid:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    data = request.get_json()
    appt = db.query(Appointment).filter_by(appointment_id=appointment_id).first()
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    appt.title = data.get("title", appt.title)
    appt.date_time = (
        datetime.fromisoformat(data["date_time"])
        if "date_time" in data
        else appt.date_time
    )
    appt.location = data.get("location", appt.location)
    db.commit()
    return jsonify({"message": "Appointment updated"})


# Delete appointment
@appointments_bp.route("/appointments/<uuid:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appt = db.query(Appointment).filter_by(appointment_id=appointment_id).first()
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404
    db.delete(appt)
    db.commit()
    return jsonify({"message": "Appointment deleted"})
