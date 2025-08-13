from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Medication, db, User, CaregiverAssignment
from datetime import datetime
from tasks import send_medication_reminder
from flask import request

from schemas.medication import (
    MedicationSchema,
    MedicationResponseSchema,
    MedicationAddResponseSchema,
)

from flask_security import roles_accepted

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

        session = db.session
        try:
            medication = Medication(
                name=data["name"],
                dosage=data["dosage"],
                time=datetime.fromisoformat(data["time"]),
                isTaken=data.get("isTaken", False),
                senior_id=senior_id,
            )
            session.add(medication)
            session.commit()
            send_medication_reminder.apply_async(
                args=[str(medication.medication_id)], eta=medication.time
            )
            return {
                "message": "Medication added",
                "medication_id": medication.medication_id,
            }
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()


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
        senior_id = MedicationsResource.get_senior_id_from_user(user_id)
        session = db.session
        try:
            med = (
                session.query(Medication)
                .filter_by(medication_id=medication_id, senior_id=senior_id)
                .first()
            )
            if not med:
                abort(404, message="Medication not found")

            if "name" in data:
                med.name = data["name"]
            if "dosage" in data:
                med.dosage = data["dosage"]
            if "time" in data:
                med.time = datetime.fromisoformat(data["time"])
            if "isTaken" in data:
                med.isTaken = data["isTaken"]

            session.commit()

            # --- FIX ---
            # Instead of returning the raw 'med' object which will become detached,
            # query it again to get a fresh instance that the serializer can use.
            session.refresh(med)
            return med

        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(summary="Delete a medication by ID.")
    @medications_blp.response(200, MedicationAddResponseSchema)
    def delete(self, medication_id):
        user_id = get_jwt_identity()
        senior_id = MedicationsResource.get_senior_id_from_user(user_id)
        session = db.session
        try:
            med = (
                session.query(Medication)
                .filter_by(medication_id=medication_id, senior_id=senior_id)
                .first()
            )
            if not med:
                abort(404, message="Medication not found")

            session.delete(med)
            session.commit()
            return {"message": "Medication deleted"}
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()
