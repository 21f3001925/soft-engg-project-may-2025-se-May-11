from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from marshmallow import Schema, fields
from models import db, CaregiverAssignment, Caregiver, SeniorCitizen, User

assignment_bp = Blueprint("Assignment", "Assignment", url_prefix="/api/v1/assignment")


class SeniorSchema(Schema):
    id = fields.Str(attribute="user_id")
    name = fields.Str(attribute="username")
    email = fields.Str()
    age = fields.Int()
    phone = fields.Str(attribute="phone_number")


class AssignSchema(Schema):
    senior_id = fields.Str(required=True)


@assignment_bp.route("/available-seniors")
class AvailableSeniorsAPI(MethodView):
    @jwt_required()
    @roles_accepted("caregiver")
    @assignment_bp.doc(
        summary="Get all unassigned senior citizens",
        description="Returns a list of senior citizens who do not have a caregiver assigned.",
    )
    @assignment_bp.response(200, SeniorSchema(many=True))
    def get(self):
        # Get all seniors who are NOT assigned in CaregiverAssignment
        assigned_senior_ids = [a.senior_id for a in CaregiverAssignment.query.all()]
        seniors = SeniorCitizen.query.filter(
            ~SeniorCitizen.user_id.in_(assigned_senior_ids)
        ).all()
        # Return their User info
        users = [User.query.get(s.user_id) for s in seniors]
        return users


@assignment_bp.route("/assign", methods=["POST"])
class AssignCaregiverAPI(MethodView):
    @jwt_required()
    @roles_accepted("caregiver")
    @assignment_bp.doc(
        summary="Assign yourself (caregiver) to a senior citizen",
        description="Assigns the currently logged-in caregiver to the specified senior citizen. Only works if the senior is not already assigned.",
    )
    @assignment_bp.arguments(AssignSchema)
    @assignment_bp.response(201)
    def post(self, data):
        caregiver_id = get_jwt_identity()
        senior_id = data["senior_id"]

        # Ensure only one caregiver per senior
        existing = CaregiverAssignment.query.filter_by(senior_id=senior_id).first()
        if existing:
            abort(400, message="This senior already has a caregiver assigned.")

        # Ensure caregiver and senior exist
        caregiver = Caregiver.query.get(caregiver_id)
        senior = SeniorCitizen.query.get(senior_id)
        if not caregiver or not senior:
            abort(404, message="Caregiver or Senior not found.")

        assignment = CaregiverAssignment(caregiver_id=caregiver_id, senior_id=senior_id)
        db.session.add(assignment)
        db.session.commit()
        return {"message": "Caregiver assigned to senior."}, 201


@assignment_bp.route("/my-seniors")
class MySeniorsAPI(MethodView):
    @jwt_required()
    @roles_accepted("caregiver")
    @assignment_bp.doc(
        summary="Get all seniors assigned to the current caregiver",
        description="Returns a list of senior citizens assigned to the currently logged-in caregiver.",
    )
    @assignment_bp.response(200, SeniorSchema(many=True))
    def get(self):
        caregiver_id = get_jwt_identity()
        assignments = CaregiverAssignment.query.filter_by(
            caregiver_id=caregiver_id
        ).all()
        seniors = []
        for assignment in assignments:
            senior_user = User.query.get(assignment.senior_id)
            if senior_user:
                seniors.append(senior_user)
        return seniors
