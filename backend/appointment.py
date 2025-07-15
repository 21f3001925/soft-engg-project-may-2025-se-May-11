# appointment.py
from flask import Blueprint, request, jsonify
from models import Appointment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

from tasks import send_reminder_notification

appointment_bp = Blueprint("appointments", __name__)
db = SQLAlchemy()

@appointment_bp.route("/appointments", methods=["GET"])
def get_appointments():
    appts = db.session.query(Appointment).all()
    return jsonify([
        {
            "appointment_id": str(a.appointment_id),
            "title": a.title,
            "date_time": a.date_time.isoformat(),
            "location": a.location,
            "senior_id": str(a.senior_id),
            "reminder_time": a.reminder_time.isoformat() if a.reminder_time else None
        }
        for a in appts
    ])

@appointment_bp.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()
    try:
        appt = Appointment(
            appointment_id=uuid.uuid4(),
            title=data["title"],
            date_time=datetime.fromisoformat(data["date_time"]),
            location=data["location"],
            senior_id=uuid.UUID(data["senior_id"]),
            reminder_time=datetime.fromisoformat(data["reminder_time"]) if "reminder_time" in data else None,
        )
        db.session.add(appt)
        db.session.commit()

        if appt.reminder_time:
            send_reminder_notification.apply_async(
                args=[str(appt.appointment_id), appt.title, appt.location, appt.date_time.isoformat()],
                eta=appt.reminder_time
            )

        return jsonify({"message": "Appointment created", "id": str(appt.appointment_id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@appointment_bp.route("/appointments/<uuid:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    data = request.get_json()
    appt = db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    appt.title = data.get("title", appt.title)
    appt.date_time = datetime.fromisoformat(data["date_time"]) if "date_time" in data else appt.date_time
    appt.location = data.get("location", appt.location)
    if "reminder_time" in data:
        appt.reminder_time = datetime.fromisoformat(data["reminder_time"])

    db.session.commit()

    if appt.reminder_time:
        send_reminder_notification.apply_async(
            args=[str(appt.appointment_id), appt.title, appt.location, appt.date_time.isoformat()],
            eta=appt.reminder_time
        )

    return jsonify({"message": "Appointment updated"})

@appointment_bp.route("/appointments/<uuid:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appt = db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appt)
    db.session.commit()
    return jsonify({"message": "Appointment deleted"})
