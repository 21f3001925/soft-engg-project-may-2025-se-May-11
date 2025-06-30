from flask import Blueprint, request, jsonify
from models import Medication
from datetime import datetime
from db_session import Session
from flask_jwt_extended import jwt_required, get_jwt_identity

medications_bp = Blueprint('medications', __name__)

@medications_bp.route('/medications', methods=['GET', 'POST'])
@jwt_required()
def medications():
    session = Session()
    if request.method == "POST":
        data = request.get_json()
        try:
            medication = Medication(
                name=data["name"],
                dosage=data["dosage"],
                time=datetime.fromisoformat(data["time"]),
                isTaken=data.get("isTaken", False),
                senior_id=data["senior_id"]
            )
            session.add(medication)
            session.commit()
            return jsonify({"message": "Medication added", "medication_id": medication.medication_id}), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            session.close()
    else:
        meds = session.query(Medication).all()
        result = [
            {
                "medication_id": m.medication_id,
                "name": m.name,
                "dosage": m.dosage,
                "time": m.time.isoformat() if m.time else None,
                "isTaken": m.isTaken,
                "senior_id": m.senior_id
            } for m in meds
        ]
        session.close()
        return jsonify(result)
