from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from flask import request
from models import Appointment, db, User, CaregiverAssignment
import pytz

import uuid
from tasks import send_reminder_notification
from celery_app import celery_app
from schemas.appointments import (
    AppointmentSchema,
    AppointmentResponseSchema,
    AppointmentAddResponseSchema,
    AppointmentStatusUpdateSchema,
)

appointments_blp = Blueprint(
    "Appointments",
    "Appointments",
    url_prefix="/api/v1/appointments",
    description="This route is essential for managing appointments. It provides comprehensive endpoints for creating, viewing, updating, and deleting appointment details. This functionality is crucial for helping both seniors and their caregivers keep track of medical check-ups and other important dates, ensuring that no appointments are missed and that seniors can stay prepared for upcoming events.",
)


class AppointmentUtils:
    @staticmethod
    def get_senior_id(user_id, requested_senior_id=None):
        user = User.query.get(user_id)
        if user.roles[0].name == "senior_citizen":
            # If a specific senior's resource is requested, ensure the
            # logged-in senior is that same person.
            if requested_senior_id and str(user.user_id) != str(requested_senior_id):
                abort(403, message="You are not authorized to access this resource.")
            return user.user_id

        elif user.caregiver:
            # If specific senior_id is requested, validate caregiver has access
            if requested_senior_id:
                assignment = CaregiverAssignment.query.filter_by(
                    caregiver_id=str(user.user_id), senior_id=str(requested_senior_id)
                ).first()

                if assignment:
                    return requested_senior_id
                else:
                    abort(403, message="You are not assigned to this senior citizen.")

            # If no specific senior requested, return first assigned senior (backward compatibility)
            assignments = CaregiverAssignment.query.filter_by(
                caregiver_id=user.user_id
            ).all()
            if assignments:
                return assignments[0].senior_id
            else:
                abort(404, message="Caregiver is not assigned to any senior citizen.")
        abort(404, message="Senior citizen not found.")


@appointments_blp.route("")
class AppointmentListResource(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "caregiver")
    @appointments_blp.response(200, AppointmentResponseSchema(many=True))
    @appointments_blp.doc(
        summary="Get information about all the appointments of the specified or logged in senior citizen."
    )
    def get(self):
        user_id = get_jwt_identity()
        # Get senior_id from query parameter if provided
        requested_senior_id = request.args.get("senior_id")
        senior_id = AppointmentUtils.get_senior_id(user_id, requested_senior_id)
        # Convert to string for SQLite compatibility
        appointments = Appointment.query.filter_by(senior_id=str(senior_id)).all()
        return appointments

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.arguments(AppointmentSchema)
    @appointments_blp.response(201, AppointmentAddResponseSchema)
    @appointments_blp.doc(
        summary="Add a new appointment for the specified or logged in senior citizen."
    )
    def post(self, data):
        try:
            user_id = get_jwt_identity()
            requested_senior_id = data.get("senior_id")
            senior_id = AppointmentUtils.get_senior_id(user_id, requested_senior_id)

            senior_user = User.query.get(str(senior_id))

            local_tz = pytz.timezone("Asia/Kolkata")

            # Make the incoming naive datetime aware of its local timezone (IST)
            aware_date_time = local_tz.localize(data["date_time"])

            appointment = Appointment(
                appointment_id=str(uuid.uuid4()),
                title=data["title"],
                # Convert the aware local time to UTC before saving to the DB
                date_time=aware_date_time.astimezone(pytz.utc),
                location=data["location"],
                reminder_time=data.get("reminder_time"),
                senior_id=str(senior_id),
            )

            if appointment.reminder_time:
                # This part for the reminder remains the same
                aware_reminder_time = local_tz.localize(appointment.reminder_time)
                task = send_reminder_notification.apply_async(
                    args=[
                        str(appointment.appointment_id),
                        appointment.title,
                        appointment.location,
                        # Pass the original ISO format for display purposes
                        aware_date_time.isoformat(),
                        senior_user.email,
                    ],
                    eta=aware_reminder_time,
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
    @appointments_blp.doc(
        summary="To get information about a specific appointment, user can use this endpoint with appointment_id."
    )
    def get(self, appointment_id):
        user_id = get_jwt_identity()

        appt = Appointment.query.filter_by(appointment_id=str(appointment_id)).first()
        if not appt:
            abort(404, message="Appointment not found")

        # Validate access to this appointment
        try:
            AppointmentUtils.get_senior_id(user_id, appt.senior_id)
        except PermissionError:
            abort(403, message="You are not authorized to view this appointment.")

        return appt

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.arguments(AppointmentSchema(partial=True))
    @appointments_blp.response(200, AppointmentResponseSchema)
    @appointments_blp.doc(
        summary="When details of an appointment change, user can update it using appointment_id."
    )
    def put(self, data, appointment_id):
        user_id = get_jwt_identity()

        appt = Appointment.query.filter_by(appointment_id=str(appointment_id)).first()
        if not appt:
            abort(404, message="Appointment not found")

        # Validate access to this appointment
        try:
            AppointmentUtils.get_senior_id(user_id, appt.senior_id)
        except PermissionError:
            abort(403, message="You are not authorized to modify this appointment.")

        for field in ["title", "location"]:
            if field in data:
                setattr(appt, field, data[field])

        time_updated = False
        local_tz = pytz.timezone("Asia/Kolkata")

        if "date_time" in data:
            time_updated = True

            dt_from_request = data["date_time"]
            if dt_from_request.tzinfo is None:
                # If naive, localize it to the server's timezone
                aware_date_time = local_tz.localize(dt_from_request)
            else:
                # If already aware, use it directly
                aware_date_time = dt_from_request

            # Always store in UTC
            appt.date_time = aware_date_time.astimezone(pytz.utc)

        if "reminder_time" in data:
            time_updated = True

        if time_updated and appt.status == "Missed":
            appt.status = "Scheduled"
            senior_user = User.query.get(str(appt.senior_id))
            if senior_user and senior_user.senior_citizen:
                senior_user.senior_citizen.appointments_missed = max(
                    0, senior_user.senior_citizen.appointments_missed - 1
                )
                db.session.add(senior_user.senior_citizen)

        if appt.reminder_task_id:
            celery_app.control.revoke(appt.reminder_task_id)
            appt.reminder_task_id = None

        if "reminder_time" in data and data["reminder_time"] is not None:
            appt.reminder_time = data["reminder_time"]
            senior_user = User.query.get(str(appt.senior_id))

            reminder_dt = appt.reminder_time
            if reminder_dt.tzinfo is None:
                # If naive, localize it
                aware_reminder_time = local_tz.localize(reminder_dt)
            else:
                aware_reminder_time = reminder_dt

            task = send_reminder_notification.apply_async(
                args=[
                    str(appt.appointment_id),
                    appt.title,
                    appt.location,
                    appt.date_time.isoformat(),
                    senior_user.email,
                ],
                eta=aware_reminder_time,
            )
            appt.reminder_task_id = task.id

        db.session.add(appt)
        db.session.commit()
        return appt

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.arguments(AppointmentStatusUpdateSchema)
    @appointments_blp.response(200, AppointmentResponseSchema)
    @appointments_blp.doc(
        summary="Update appointment status (e.g., mark as completed)."
    )
    def patch(self, data, appointment_id):
        user_id = get_jwt_identity()

        appt = Appointment.query.filter_by(appointment_id=str(appointment_id)).first()
        if not appt:
            abort(404, message="Appointment not found")

        # Validate access to this appointment
        try:
            AppointmentUtils.get_senior_id(user_id, appt.senior_id)
        except PermissionError:
            abort(403, message="You are not authorized to modify this appointment.")

        if "status" in data:
            new_status = data["status"]

            if new_status == "Completed":
                if appt.status == "Completed":
                    abort(400, message="Appointment is already completed.")

                senior_user = User.query.get(str(appt.senior_id))
                if not senior_user or not senior_user.senior_citizen:
                    abort(404, message="Senior citizen not found.")

                previous_status = appt.status
                appt.status = "Completed"

                if (
                    previous_status == "Missed"
                    and senior_user.senior_citizen.appointments_missed > 0
                ):
                    senior_user.senior_citizen.appointments_missed = max(
                        0, senior_user.senior_citizen.appointments_missed - 1
                    )

                if appt.reminder_task_id:
                    celery_app.control.revoke(appt.reminder_task_id)
                    appt.reminder_task_id = None

                db.session.add(senior_user.senior_citizen)
            else:
                appt.status = new_status

        db.session.add(appt)
        db.session.commit()
        return appt

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @appointments_blp.response(200, AppointmentAddResponseSchema)
    @appointments_blp.doc(
        summary="User can delete a specific appointment by ID whenever it is not needed."
    )
    def delete(self, appointment_id):
        user_id = get_jwt_identity()

        appt = Appointment.query.filter_by(appointment_id=str(appointment_id)).first()
        if not appt:
            abort(404, message="Appointment not found")

        # Validate access to this appointment
        try:
            AppointmentUtils.get_senior_id(user_id, appt.senior_id)
        except PermissionError:
            abort(403, message="You are not authorized to delete this appointment.")

        if appt.reminder_task_id:
            celery_app.control.revoke(appt.reminder_task_id)

        db.session.delete(appt)
        db.session.commit()
        return {"message": "Appointment deleted"}, 200
