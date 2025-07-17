from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models import Medication, db
from datetime import datetime

from schemas.medication import (
    MedicationSchema,
    MedicationResponseSchema,
    MedicationAddResponseSchema,
)
from flask_security import roles_accepted


medications_blp = Blueprint(
    "medications", "medications", url_prefix="/api/v1/medications"
)


@medications_blp.route("")
class MedicationsResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @medications_blp.response(200, MedicationResponseSchema(many=True))
    def get(self):

        session = db.session
        meds = db.session.query(Medication).all()
        result = [
            {
                "medication_id": m.medication_id,
                "name": m.name,
                "dosage": m.dosage,
                "time": m.time.isoformat() if m.time else None,
                "isTaken": m.isTaken,
                "senior_id": m.senior_id,
            }
            for m in meds
        ]
        session.close()
        return result

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @medications_blp.arguments(MedicationSchema())
    @medications_blp.response(201, MedicationAddResponseSchema())
    @medications_blp.alt_response(400, schema=MedicationAddResponseSchema())
    def post(self, data):
        session = db.session
        try:
            medication = Medication(
                name=data["name"],
                dosage=data["dosage"],
                time=datetime.fromisoformat(data["time"]),
                isTaken=data.get("isTaken", False),
                senior_id=data["senior_id"],
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
