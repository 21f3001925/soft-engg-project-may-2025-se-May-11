from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from models import db, Event, EventAttendance, User
from marshmallow import Schema, fields
from tasks import send_event_reminder
from datetime import datetime
import pytz


class EventSchema(Schema):
    event_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    # This MUST have format='iso'
    date_time = fields.DateTime(format="iso", required=True)
    location = fields.Str(required=True)
    description = fields.Str()
    service_provider_id = fields.Str()

    class Meta:
        unknown = "exclude"


class EventJoinSchema(Schema):
    event_id = fields.Str(required=True)
    senior_id = fields.Str(required=False)


class AttendeeSchema(Schema):
    user_id = fields.Str()
    name = fields.Str()
    email = fields.Str()


events_bp = Blueprint(
    "Events",
    "Events",
    url_prefix="/api/v1/events",
    description="This route manages social events for senior citizens. It allows service providers to create, update, and delete event listings, while enabling seniors to browse and join activities. This feature is designed to promote social engagement and help seniors stay active and connected with their community.",
)


@events_bp.route("")
class EventList(MethodView):
    @jwt_required()
    @roles_accepted("service_provider", "senior_citizen")
    @events_bp.response(200, EventSchema(many=True))
    def get(self):
        events = Event.query.all()
        return events

    @events_bp.arguments(EventSchema)
    @events_bp.response(201, EventSchema)
    def post(self, new_data):
        event = Event(**new_data)
        db.session.add(event)
        db.session.commit()
        return event


@events_bp.route("/<string:event_id>")
class EventResource(MethodView):
    @jwt_required()
    @roles_accepted("service_provider", "senior_citizen")
    @events_bp.response(200, EventSchema)
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return event

    @events_bp.arguments(EventSchema(partial=True))
    @events_bp.response(200, EventSchema)
    def put(self, update_data, event_id):
        event = Event.query.get_or_404(event_id)
        for key, value in update_data.items():
            setattr(event, key, value)
        db.session.commit()
        return event

    @jwt_required()
    @roles_accepted("service_provider")
    @events_bp.doc(
        summary="To delete an event, service provider can use this route with the event id."
    )
    @events_bp.response(204)
    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()


@events_bp.route("/join")
class EventJoin(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen")
    @events_bp.doc(
        summary="When senior citizens see the event list, they might want to join an event. They can use this route to join an event."
    )
    @events_bp.arguments(EventJoinSchema)
    @events_bp.response(
        200, description="Successfully joined event and reminder scheduled"
    )
    @events_bp.alt_response(400, description="Bad Request")
    @events_bp.alt_response(404, description="Event not found")
    @events_bp.alt_response(409, description="Already joined event")
    def post(self, data):
        senior_id = get_jwt_identity()
        event_id = data["event_id"]

        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found")

        # Check if already attending
        existing_attendance = EventAttendance.query.filter_by(
            senior_id=senior_id, event_id=event_id
        ).first()
        if existing_attendance:
            abort(409, message="You have already joined this event.")

        # Create attendance
        attendance = EventAttendance(senior_id=senior_id, event_id=event_id)
        db.session.add(attendance)
        db.session.commit()

        # --- SIMPLIFIED SCHEDULING ---
        now_utc = datetime.now(pytz.UTC)

        # The datetime from the DB is now reliably UTC.
        # Ensure it's timezone-aware for comparison.
        if event.date_time.tzinfo is None:
            # This handles the case where SQLite might store naive datetimes
            event_time_utc = pytz.UTC.localize(event.date_time)
        else:
            event_time_utc = event.date_time

        print(f"DEBUG - Current UTC: {now_utc}")
        print(f"DEBUG - Event time UTC from DB: {event_time_utc}")

        if event_time_utc > now_utc:
            delay_seconds = (event_time_utc - now_utc).total_seconds()

            # For the task, we can still format it nicely for the user message.
            ist_tz = pytz.timezone("Asia/Kolkata")
            event_time_ist_display = event_time_utc.astimezone(ist_tz)

            task_args = [
                senior_id,
                event.name,
                event.location,
                event_time_ist_display.isoformat(),  # Pass IST string for display
            ]

            print(f"DEBUG - Scheduling reminder in {delay_seconds:.2f} seconds")
            result = send_event_reminder.apply_async(
                args=task_args, countdown=delay_seconds
            )
            print(f"DEBUG - Task scheduled with ID: {result.id}")
        else:
            print("DEBUG - Event is in the past, not scheduling reminder")

        return {"message": "Successfully joined event and reminder scheduled"}, 200


class JoinedEventsSchema(Schema):
    event_ids = fields.List(fields.Str())


@events_bp.route("/joined")
class JoinedEvents(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen")
    @events_bp.doc(
        summary="Get all event IDs the current senior citizen has joined.",
        description="Returns a list of event IDs that the currently authenticated senior citizen has joined. Useful for displaying which events the user is attending.",
    )
    @events_bp.response(200, JoinedEventsSchema)
    def get(self):
        senior_id = get_jwt_identity()
        joined = EventAttendance.query.filter_by(senior_id=senior_id).all()
        event_ids = [ea.event_id for ea in joined]
        return {"event_ids": event_ids}


@events_bp.route("/unjoin", methods=["POST"])
class EventUnjoin(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen", "service_provider")
    @events_bp.doc(
        summary="Cancel event attendance for a senior citizen.",
        description="Allows a senior citizen to cancel their attendance for an event, or a service provider to remove a senior from an event by specifying both event_id and senior_id.",
    )
    @events_bp.arguments(EventJoinSchema)
    @events_bp.response(200, description="Successfully cancelled event attendance")
    @events_bp.alt_response(404, description="Attendance not found")
    def post(self, data):
        event_id = data["event_id"]
        # For provider, allow specifying senior_id; for senior, use their own id
        senior_id = data.get("senior_id") or get_jwt_identity()

        attendance = EventAttendance.query.filter_by(
            senior_id=senior_id, event_id=event_id
        ).first()
        if not attendance:
            abort(404, message="You are not attending this event.")

        db.session.delete(attendance)
        db.session.commit()
        return {"message": "Successfully cancelled event attendance"}, 200


@events_bp.route("/<string:event_id>/attendees")
class EventAttendees(MethodView):
    @jwt_required()
    @roles_accepted("service_provider")
    @events_bp.doc(
        summary="Get list of attendees for a specific event.",
        description="Returns a list of users (with name and email) who have joined the specified event. Only accessible by service providers.",
    )
    @events_bp.response(200, AttendeeSchema(many=True))
    def get(self, event_id):
        # Get all EventAttendance records for this event
        attendances = EventAttendance.query.filter_by(event_id=event_id).all()
        # Get the User records for each senior_id
        seniors = User.query.filter(
            User.user_id.in_([a.senior_id for a in attendances])
        ).all()
        # Return their basic info
        return [
            {"user_id": s.user_id, "name": s.username, "email": s.email}
            for s in seniors
        ]
