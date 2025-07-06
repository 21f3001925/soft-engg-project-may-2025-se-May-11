from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models import Medication
from datetime import datetime
from db_session import Session
from marshmallow import Schema, fields


class MedicationSchema(Schema):
    name = fields.Str(required=True)
    dosage = fields.Str(required=True)
    time = fields.Str(required=True)
    isTaken = fields.Boolean(missing=False)
    senior_id = fields.Int(required=True)


class MedicationResponseSchema(Schema):
    medication_id = fields.Int()
    name = fields.Str()
    dosage = fields.Str()
    time = fields.Str()
    isTaken = fields.Boolean()
    senior_id = fields.Int()


class MedicationAddResponseSchema(Schema):
    message = fields.Str()
    medication_id = fields.Int()


medications_blp = Blueprint(
    "medications", "medications", url_prefix="/api/v1/medications"
)


@medications_blp.route("")
class MedicationsResource(MethodView):
    @jwt_required()
    @medications_blp.response(200, MedicationResponseSchema(many=True))
    def get(self):
        session = Session()
        meds = session.query(Medication).all()
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
    @medications_blp.arguments(MedicationSchema())
    @medications_blp.response(201, MedicationAddResponseSchema())
    @medications_blp.alt_response(400, schema=MedicationAddResponseSchema())
    def post(self, data):
        session = Session()
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
