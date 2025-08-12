from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from models import db, Event, EventAttendance, User
from marshmallow import Schema, fields
from tasks import send_event_reminder
from datetime import timedelta, datetime


class EventSchema(Schema):
    event_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.Str(required=True)
    description = fields.Str()
    service_provider_id = fields.Str()

    class Meta:
        unknown = "exclude"


class EventJoinSchema(Schema):
    event_id = fields.Str(required=True)
    senior_id = fields.Str(required=False)  # Optional for provider


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
    @events_bp.doc(
        summary="All events organised by various service providers are listed when the route is called."
    )
    @events_bp.response(200, EventSchema(many=True))
    def get(self):
        events = Event.query.all()
        return events

    @events_bp.doc(summary="Service provider can add a new event using this endpoint.")
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
    @events_bp.doc(
        summary="To get specific event details, service provider can use this route with the event id."
    )
    @events_bp.response(200, EventSchema)
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return event

    @events_bp.doc(
        summary="To update event details, service provider can use this route with the event id."
    )
    @events_bp.arguments(EventSchema(partial=True))
    @events_bp.response(200, EventSchema)
    def put(self, update_data, event_id):
        event = Event.query.get_or_404(event_id)
        for key, value in update_data.items():
            if key == "date_time":
                if isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
                    except Exception:
                        continue
                if not isinstance(value, datetime):
                    continue
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

        # Check if senior is already attending
        existing_attendance = EventAttendance.query.filter_by(
            senior_id=senior_id, event_id=event_id
        ).first()
        if existing_attendance:
            abort(409, message="You have already joined this event.")

        # Create attendance record
        attendance = EventAttendance(senior_id=senior_id, event_id=event_id)
        db.session.add(attendance)
        db.session.commit()

        # Schedule event reminder (e.g., 1 hour before the event)
        reminder_time = event.date_time - timedelta(hours=1)
        if reminder_time > datetime.utcnow():  # Only schedule if in the future
            send_event_reminder.apply_async(
                args=[
                    senior_id,
                    event.name,
                    event.location,
                    event.date_time.isoformat(),
                ],
                eta=reminder_time,
            )

        return {"message": "Successfully joined event and reminder scheduled"}, 200


class JoinedEventsSchema(Schema):
    event_ids = fields.List(fields.Str())


@events_bp.route("/joined")
class JoinedEvents(MethodView):
    @jwt_required()
    @roles_accepted("senior_citizen")
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
