from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from backend.models import db, Event
from marshmallow import Schema, fields


class EventSchema(Schema):
    event_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    date_time = fields.DateTime(required=True)
    location = fields.Str(required=True)
    description = fields.Str()
    service_provider_id = fields.Str(required=True)


events_bp = Blueprint(
    "events", "events", url_prefix="/api/v1/events", description="Operations on events"
)


@events_bp.route("/")
class EventList(MethodView):

    @jwt_required()
    @events_bp.response(200, EventSchema(many=True))
    def get(self):
        return Event.query.all()

    @jwt_required()
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
    @events_bp.response(200, EventSchema)
    def get(self, event_id):
        return Event.query.get_or_404(event_id)

    @jwt_required()
    @events_bp.arguments(EventSchema)
    @events_bp.response(200, EventSchema)
    def put(self, update_data, event_id):
        event = Event.query.get_or_404(event_id)
        for key, value in update_data.items():
            setattr(event, key, value)
        db.session.commit()
        return event

    @jwt_required()
    @events_bp.response(204)
    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
