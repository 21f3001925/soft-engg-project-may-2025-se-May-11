from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from models import db, Event, EventAttendance
from marshmallow import Schema, fields
from tasks import send_event_reminder
from datetime import timedelta, datetime


class EventSchema(Schema):
    event_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.Str(required=True)
    description = fields.Str()
    service_provider_id = fields.Str(required=True)


class EventJoinSchema(Schema):
    event_id = fields.Str(required=True)


events_bp = Blueprint(
    "Events",
    "Events",
    url_prefix="/api/v1/events",
    description="This route manages social events for senior citizens. It allows service providers to create, update, and delete event listings, while enabling seniors to browse and join activities. This feature is designed to promote social engagement and help seniors stay active and connected with their community.",
)


@events_bp.route("")
class EventList(MethodView):

    @events_bp.doc(
        summary="All events organised by various service providers are listed when the route is called."
    )
    #@events_bp.response(200, EventSchema(many=True))
    def get(self):
        events = Event.query.all()
        result = [
            {
                "event_id": event.event_id,
                "name": event.name,
                "description": event.description,
                "date_time": event.date_time.isoformat() if event.date_time else None,
                "location": event.location,
                "service_provider_id": event.service_provider_id,
            }
            for event in events
        ]
        return result

    @events_bp.doc(summary="Service provider can add a new event using this endpoint.")
    @events_bp.arguments(EventSchema)
    @events_bp.response(201, EventSchema)
    def post(self, new_data):
        event = Event(**new_data)
        db.session.add(event)
        db.session.commit()
        return {
            "event_id": event.event_id,
            "name": event.name,
            "description": event.description,
            "date_time": event.date_time.isoformat() if event.date_time else None,
            "location": event.location,
            "service_provider_id": event.service_provider_id,
        }


@events_bp.route("/<string:event_id>")
class EventResource(MethodView):

    @events_bp.doc(
        summary="To get specific event details, service provider can use this route with the event id."
    )
    @events_bp.response(200, EventSchema)
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return {
            "event_id": event.event_id,
            "name": event.name,
            "description": event.description,
            "date_time": event.date_time.isoformat() if event.date_time else None,
            "location": event.location,
            "service_provider_id": event.service_provider_id,
        }

    @events_bp.doc(
        summary="To update event details, service provider can use this route with the event id."
    )
    @events_bp.arguments(EventSchema(partial=True))
    @events_bp.response(200, EventSchema)
    def put(self, update_data, event_id):
        event = Event.query.get_or_404(event_id)
        for key, value in update_data.items():
            setattr(event, key, value)
        db.session.commit()
        return {
            "event_id": event.event_id,
            "name": event.name,
            "description": event.description,
            "date_time": event.date_time.isoformat() if event.date_time else None,
            "location": event.location,
            "service_provider_id": event.service_provider_id,
        }

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
