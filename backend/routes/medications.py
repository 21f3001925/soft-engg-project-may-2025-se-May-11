from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Medication, db, User, CaregiverAssignment
from datetime import datetime
from tasks import (
    send_medication_reminder,
    celery_app,
    notify_caregiver_medication_taken,
)
from flask import request
import pytz


from schemas.medication import (
    MedicationSchema,
    MedicationResponseSchema,
    MedicationAddResponseSchema,
)

from flask_security import roles_accepted

IST = pytz.timezone("Asia/Kolkata")

medications_blp = Blueprint(
    "Medications",
    "Medications",
    url_prefix="/api/v1/medications",
    description="This route is responsible for managing medication schedules...",
)


@medications_blp.route("")
class MedicationsResource(MethodView):
    @staticmethod
    def get_senior_id_from_user(user_id):
        user = User.query.get(user_id)
        user_roles = [role.name for role in user.roles]

        if "senior_citizen" in user_roles:
            return user.user_id

        elif "caregiver" in user_roles:
            senior_id = request.args.get("senior_id")
            if not senior_id:
                abort(
                    400,
                    message="A 'senior_id' query parameter is required for caregivers.",
                )

            # --- AUTHORIZATION CHECK ---
            is_authorized = (
                db.session.query(CaregiverAssignment)
                .filter_by(caregiver_id=user.user_id, senior_id=senior_id)
                .first()
            )
            if not is_authorized:
                abort(
                    403, message="You are not authorized to access this senior's data."
                )

            return senior_id
        else:
            abort(404, message="Senior citizen not found or user role is invalid.")

    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @medications_blp.doc(
        summary="Get all medications for the specified senior citizen."
    )
    @medications_blp.response(200, MedicationResponseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        senior_id = self.get_senior_id_from_user(user_id)
        session = db.session
        try:
            return session.query(Medication).filter_by(senior_id=senior_id).all()
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(
        summary="Add a new medication for the specified senior citizen."
    )
    @medications_blp.arguments(MedicationSchema())
    @medications_blp.response(201, MedicationAddResponseSchema())
    def post(self, data):
        user_id = get_jwt_identity()
        senior_id = self.get_senior_id_from_user(user_id)
        # medication_time = datetime.fromisoformat(data["time"])

        naive_datetime = datetime.fromisoformat(data["time"])
        local_datetime = IST.localize(naive_datetime)  # Assume the time sent is IST

        medication = Medication(
            name=data["name"],
            dosage=data["dosage"],
            time=local_datetime,
            isTaken=data.get("isTaken", False),
            senior_id=senior_id,
        )

        # Schedule the reminder and store the task ID
        result = send_medication_reminder.apply_async(
            args=[str(medication.medication_id)], eta=local_datetime
        )
        medication.reminder_task_id = result.id

        db.session.add(medication)
        db.session.commit()

        return {
            "message": "Medication added and reminder scheduled",
            "medication_id": medication.medication_id,
        }


@medications_blp.route("/<string:medication_id>")
class MedicationByIdResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @medications_blp.doc(summary="Get a specific medication by ID.")
    @medications_blp.response(200, MedicationResponseSchema)
    def get(self, medication_id):
        user_id = get_jwt_identity()
        senior_id = MedicationsResource.get_senior_id_from_user(user_id)
        med = (
            db.session.query(Medication)
            .filter_by(medication_id=medication_id, senior_id=senior_id)
            .first()
        )
        if not med:
            abort(404, message="Medication not found")
        return med

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(summary="Update a medication by ID.")
    @medications_blp.arguments(MedicationSchema(partial=True))
    @medications_blp.response(200, MedicationResponseSchema)
    def put(self, data, medication_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        user_roles = [role.name for role in user.roles]

        if "isTaken" in data:
            if "caregiver" in user_roles:
                abort(
                    403,
                    message="Caregivers are not authorized to change the 'taken' status.",
                )

        senior_id = MedicationsResource.get_senior_id_from_user(user_id)
        med = (
            db.session.query(Medication)
            .filter_by(medication_id=medication_id, senior_id=senior_id)
            .first()
        )

        if not med:
            abort(404, message="Medication not found")

        if "time" in data:
            # --- THIS IS THE FIX ---
            # Parse the datetime string from the frontend
            parsed_datetime = datetime.fromisoformat(data["time"])

            # Check if the datetime is "naive" (no timezone) or "aware" (has timezone)
            if parsed_datetime.tzinfo is None:
                # If it's naive (e.g., "2025-08-14T23:16"), localize it to IST
                new_time = IST.localize(parsed_datetime)
            else:
                # If it's already aware (e.g., from .toISOString()), just use it
                new_time = parsed_datetime

            if new_time != med.time:
                if med.reminder_task_id:
                    celery_app.control.revoke(med.reminder_task_id)
                result = send_medication_reminder.apply_async(
                    args=[medication_id], eta=new_time
                )
                med.reminder_task_id = result.id
            med.time = new_time

        # --- The rest of the function remains the same ---
        if "isTaken" in data and data["isTaken"] is True and med.isTaken is False:
            notify_caregiver_medication_taken.apply_async(args=[medication_id])
            if med.reminder_task_id:
                celery_app.control.revoke(med.reminder_task_id)
                med.reminder_task_id = None

        if "name" in data:
            med.name = data["name"]
        if "dosage" in data:
            med.dosage = data["dosage"]
        if "isTaken" in data:
            med.isTaken = data["isTaken"]

        db.session.commit()
        db.session.refresh(med)
        return med

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(summary="Delete a medication by ID.")
    @medications_blp.response(200, MedicationAddResponseSchema)
    def delete(self, medication_id):
        user_id = get_jwt_identity()
        senior_id = MedicationsResource.get_senior_id_from_user(user_id)
        med = (
            db.session.query(Medication)
            .filter_by(medication_id=medication_id, senior_id=senior_id)
            .first()
        )

        if not med:
            abort(404, message="Medication not found")

        # --- REVOKE THE TASK BEFORE DELETING ---
        if med.reminder_task_id:
            celery_app.control.revoke(med.reminder_task_id)

        db.session.delete(med)
        db.session.commit()
        return {"message": "Medication deleted"}
