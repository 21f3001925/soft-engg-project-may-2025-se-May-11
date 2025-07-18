from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Medication, db, User
from datetime import datetime

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
    description="Operations on medications",
)


@medications_blp.route("")
class MedicationsResource(MethodView):
    @staticmethod
    def get_senior_id_from_user(user_id):
        user = User.query.get(user_id)
        if user.roles[0].name == "senior_citizen":
            return user.user_id
        elif user.senior_citizen:
            return user.senior_citizen.user_id
        else:
            abort(404, message="Senior citizen not found")

    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @medications_blp.doc(summary="Get all medications of the logged in senior citizen")
    @medications_blp.response(200, MedicationResponseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        senior_id = self.get_senior_id_from_user(user_id)

        session = db.session
        try:
            meds = session.query(Medication).filter_by(senior_id=senior_id).all()
            result = [
                {
                    "medication_id": med.medication_id,
                    "name": med.name,
                    "dosage": med.dosage,
                    "time": med.time.isoformat() if med.time else None,
                    "isTaken": med.isTaken,
                    "senior_id": med.senior_id,
                }
                for med in meds
            ]
        finally:
            session.close()
        return result

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(
        summary="Add a new medication for the logged in senior citizen"
    )
    @medications_blp.arguments(MedicationSchema())
    @medications_blp.response(201, MedicationAddResponseSchema())
    @medications_blp.alt_response(400, schema=MedicationAddResponseSchema())
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
            resp = {
                "message": "Medication added",
                "medication_id": medication.medication_id,
            }
            return resp, 201
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()


@medications_blp.route("/<string:medication_id>")
class MedicationByIdResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @medications_blp.doc(summary="Get a specific medication by ID")
    @medications_blp.response(200, MedicationResponseSchema)
    def get(self, medication_id):
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
            return {
                "medication_id": med.medication_id,
                "name": med.name,
                "dosage": med.dosage,
                "time": med.time.isoformat() if med.time else None,
                "isTaken": med.isTaken,
                "senior_id": med.senior_id,
            }
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(summary="Update a specific medication by ID")
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
            # Update fields
            if "name" in data:
                med.name = data["name"]
            if "dosage" in data:
                med.dosage = data["dosage"]
            if "time" in data:
                med.time = datetime.fromisoformat(data["time"])
            if "isTaken" in data:
                med.isTaken = data["isTaken"]
            session.commit()
            return {
                "medication_id": med.medication_id,
                "name": med.name,
                "dosage": med.dosage,
                "time": med.time.isoformat() if med.time else None,
                "isTaken": med.isTaken,
                "senior_id": med.senior_id,
            }
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.doc(summary="Delete a specific medication by ID")
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
            return {"message": "Medication deleted"}, 200
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()
