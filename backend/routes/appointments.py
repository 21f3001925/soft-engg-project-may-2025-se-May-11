from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from models import Appointment, db, User
from datetime import datetime
import uuid
from tasks import send_reminder_notification
from celery_app import celery_app
from schemas.appointments import (
    AppointmentSchema,
    AppointmentResponseSchema,
    AppointmentAddResponseSchema,
)

appointments_blp = Blueprint(
    "Appointments",
    "Appointments",
    url_prefix="/api/v1/appointments",
    description="The appointments route performs the CRUD operations for appointments. The user get details of the existing appointments, add information about new appointments, update and delete the existing information too. It also addresses various errors that can occur.",
)


class AppointmentUtils:
    @staticmethod
    def get_senior_id(user_id):
        user = User.query.get(user_id)
        if user.roles[0].name == "senior_citizen":
            return user.user_id
        elif user.senior_citizen:
            return user.senior_citizen.user_id
        abort(404, message="Senior citizen not found")


@appointments_blp.route("")
class AppointmentListResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @appointments_blp.response(200, AppointmentResponseSchema(many=True))
    @appointments_blp.doc(summary="Get information about all the appointments of the logged in senior citizen.")
    def get(self):
        user_id = get_jwt_identity()
        senior_id = AppointmentUtils.get_senior_id(user_id)
        appointments = Appointment.query.filter_by(senior_id=senior_id).all()
        return appointments

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.arguments(AppointmentSchema)
    @appointments_blp.response(201, AppointmentAddResponseSchema)
    @appointments_blp.doc(summary="Add a new appointment for the logged in senior citizen.")
    def post(self, data):
        try:
            user_id = get_jwt_identity()
            senior_id = AppointmentUtils.get_senior_id(user_id)
            senior_user = User.query.get(senior_id)

            appointment = Appointment(
                appointment_id=uuid.uuid4(),
                title=data["title"],
                date_time=datetime.fromisoformat(data["date_time"]),
                location=data["location"],
                reminder_time=(
                    datetime.fromisoformat(data["reminder_time"])
                    if data.get("reminder_time")
                    else None
                ),
                senior_id=senior_id,
            )

            if appointment.reminder_time:
                task = send_reminder_notification.apply_async(
                    args=[
                        str(appointment.appointment_id),
                        appointment.title,
                        appointment.location,
                        appointment.date_time.isoformat(),
                        senior_user.email,
                    ],
                    eta=appointment.reminder_time,
                )
                appointment.reminder_task_id = task.id

            db.session.add(appointment)
            db.session.commit()

            return {
                "message": "Appointment created",
                "appointment_id": str(appointment.appointment_id),
            }, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))


@appointments_blp.route("/<uuid:appointment_id>")
class AppointmentDetailResource(MethodView):
    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.response(200, AppointmentResponseSchema)
    @appointments_blp.doc(summary="To get information about a specific appointment, user can use this endpoint with appointment_id.")
    def get(self, appointment_id):
        appt = Appointment.query.filter_by(appointment_id=appointment_id).first()
        if not appt:
            abort(404, message="Appointment not found")
        return appt

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.arguments(AppointmentSchema(partial=True))
    @appointments_blp.response(200, AppointmentResponseSchema)
    @appointments_blp.doc(summary="When details of an appointment change, user can update it using appointment_id.")
    def put(self, data, appointment_id):
        appt = Appointment.query.filter_by(appointment_id=appointment_id).first()
        if not appt:
            abort(404, message="Appointment not found")

        for field in ["title", "location"]:
            if field in data:
                setattr(appt, field, data[field])
        if "date_time" in data:
            appt.date_time = datetime.fromisoformat(data["date_time"])

        if appt.reminder_task_id:
            celery_app.control.revoke(appt.reminder_task_id)

        if "reminder_time" in data:
            appt.reminder_time = datetime.fromisoformat(data["reminder_time"])
            senior_user = User.query.get(appt.senior_id)
            task = send_reminder_notification.apply_async(
                args=[
                    str(appt.appointment_id),
                    appt.title,
                    appt.location,
                    appt.date_time.isoformat(),
                    senior_user.email,
                ],
                eta=appt.reminder_time,
            )
            appt.reminder_task_id = task.id

        db.session.commit()
        return appt

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.response(200, AppointmentAddResponseSchema)
    @appointments_blp.doc(summary="User can delete a specific appointment by ID whenever it is not needed.")
    def delete(self, appointment_id):
        appt = Appointment.query.filter_by(appointment_id=appointment_id).first()
        if not appt:
            abort(404, message="Appointment not found")

        if appt.reminder_task_id:
            celery_app.control.revoke(appt.reminder_task_id)

        db.session.delete(appt)
        db.session.commit()
        return {"message": "Appointment deleted"}, 200
