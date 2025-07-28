from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import EmergencyContact, db, User

from schemas.emergency_contact import (
    EmergencyContactSchema,
    EmergencyContactResponseSchema,
    EmergencyContactAddResponseSchema,
)
from flask_security import roles_accepted

emergency_contacts_blp = Blueprint(
    "Emergency Contacts",
    "Emergency Contacts",
    url_prefix="/api/v1/emergency-contacts",
    description="This route allows users to manage a senior's emergency contacts. It provides functionality to add, view, update, and delete contact information, ensuring that the right people can be notified promptly in a crisis. This feature empowers both seniors and caregivers to maintain an up-to-date list of trusted contacts for emergency situations.",
)


@emergency_contacts_blp.route("")
class EmergencyContactsResource(MethodView):
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
    @emergency_contacts_blp.doc(
        summary="Get all emergency contacts of the logged in senior citizen"
    )
    @emergency_contacts_blp.response(200, EmergencyContactResponseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        senior_id = self.get_senior_id_from_user(user_id)

        session = db.session
        try:
            contacts = (
                session.query(EmergencyContact).filter_by(senior_id=senior_id).all()
            )
            return contacts
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @emergency_contacts_blp.doc(
        summary="Add a new emergency contact for the logged in senior citizen."
    )
    @emergency_contacts_blp.arguments(EmergencyContactSchema())
    @emergency_contacts_blp.response(201, EmergencyContactAddResponseSchema())
    @emergency_contacts_blp.alt_response(
        400, schema=EmergencyContactAddResponseSchema()
    )
    def post(self, data):
        user_id = get_jwt_identity()
        senior_id = self.get_senior_id_from_user(user_id)

        session = db.session
        try:
            contact = EmergencyContact(
                name=data["name"],
                relation=data["relation"],
                phone=data["phone"],
                senior_id=senior_id,
            )
            session.add(contact)
            session.commit()
            resp = {
                "message": "Emergency contact added",
                "contact_id": contact.contact_id,
            }
            return resp, 201
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()


@emergency_contacts_blp.route("/<string:contact_id>")
class EmergencyContactByIdResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @emergency_contacts_blp.doc(
        summary="The user can get a specific emergency contact by ID"
    )
    @emergency_contacts_blp.response(200, EmergencyContactResponseSchema)
    def get(self, contact_id):
        user_id = get_jwt_identity()
        senior_id = EmergencyContactsResource.get_senior_id_from_user(user_id)
        session = db.session
        try:
            contact = (
                session.query(EmergencyContact)
                .filter_by(contact_id=contact_id, senior_id=senior_id)
                .first()
            )
            if not contact:
                abort(404, message="Emergency contact not found")
            return contact
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @emergency_contacts_blp.doc(
        summary="When the emergency contacts change their details, user can update a specific emergency contact by ID"
    )
    @emergency_contacts_blp.arguments(EmergencyContactSchema(partial=True))
    @emergency_contacts_blp.response(200, EmergencyContactResponseSchema)
    def put(self, data, contact_id):
        user_id = get_jwt_identity()
        senior_id = EmergencyContactsResource.get_senior_id_from_user(user_id)
        session = db.session
        try:
            contact = (
                session.query(EmergencyContact)
                .filter_by(contact_id=contact_id, senior_id=senior_id)
                .first()
            )
            if not contact:
                abort(404, message="Emergency contact not found")
            # Update fields
            if "name" in data:
                contact.name = data["name"]
            if "relation" in data:
                contact.relation = data["relation"]
            if "phone" in data:
                contact.phone = data["phone"]
            session.commit()
            # Re-query to get a fresh, attached instance
            updated_contact = (
                session.query(EmergencyContact)
                .filter_by(contact_id=contact_id, senior_id=senior_id)
                .first()
            )
            return updated_contact
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @emergency_contacts_blp.doc(
        summary="User can delete a specific emergency contact by ID whenever it is not needed."
    )
    @emergency_contacts_blp.response(200, EmergencyContactAddResponseSchema)
    def delete(self, contact_id):
        user_id = get_jwt_identity()
        senior_id = EmergencyContactsResource.get_senior_id_from_user(user_id)
        session = db.session
        try:
            contact = (
                session.query(EmergencyContact)
                .filter_by(contact_id=contact_id, senior_id=senior_id)
                .first()
            )
            if not contact:
                abort(404, message="Emergency contact not found")
            session.delete(contact)
            session.commit()
            return {"message": "Emergency contact deleted"}, 200
        except Exception as e:
            session.rollback()
            abort(400, message=str(e))
        finally:
            session.close()
