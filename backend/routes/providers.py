from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted
from models import db, ServiceProvider
from routes.events import EventSchema
from marshmallow import Schema, fields


class ServiceProviderSchema(Schema):
    service_provider_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    phone_number = fields.Str()
    services_offered = fields.Str()


providers_bp = Blueprint(
    "Providers",
    "Providers",
    url_prefix="/api/v1/providers",
    description="Service providers are people who organise various activites for senior citizens. This route provides the CRUD operations for service providers. They can add, update, get, delete information about themselves. They can also get information about the events that they organise.",
)


@providers_bp.route("")
class ServiceProviderList(MethodView):

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="This route will list all the service providers and basic information about them")
    @providers_bp.response(200, ServiceProviderSchema(many=True))
    def get(self):
        return ServiceProvider.query.all()

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="To create a new service provider, this route can be used.")
    @providers_bp.arguments(ServiceProviderSchema)
    @providers_bp.response(201, ServiceProviderSchema)
    def post(self, new_data):
        provider = ServiceProvider(**new_data)
        db.session.add(provider)
        db.session.commit()
        return provider


@providers_bp.route("/<string:provider_id>")
class ServiceProviderResource(MethodView):

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="To get information about a specific service provider, this route can be used with their ID")
    @providers_bp.response(200, ServiceProviderSchema)
    def get(self, provider_id):
        return ServiceProvider.query.get_or_404(provider_id)

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="Service provider can update their information by ID")
    @providers_bp.arguments(ServiceProviderSchema)
    @providers_bp.response(200, ServiceProviderSchema)
    def put(self, update_data, provider_id):
        provider = ServiceProvider.query.get_or_404(provider_id)
        for key, value in update_data.items():
            setattr(provider, key, value)
        db.session.commit()
        return provider

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="Specific service provider can delete their information by ID")
    @providers_bp.response(204)
    def delete(self, provider_id):
        provider = ServiceProvider.query.get_or_404(provider_id)
        db.session.delete(provider)
        db.session.commit()


@providers_bp.route("/<string:provider_id>/events")
class ProviderEvents(MethodView):

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(summary="To get all events for a specific service provider, user can use this route along with service provider's ID")
    @providers_bp.response(200, EventSchema(many=True))
    def get(self, provider_id):
        provider = ServiceProvider.query.get_or_404(provider_id)
        return provider.events
