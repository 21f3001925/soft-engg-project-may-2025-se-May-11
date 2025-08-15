from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import roles_accepted
from models import db, ServiceProvider
from routes.events import EventSchema
from marshmallow import Schema, fields


class ServiceProviderSchema(Schema):
    user_id = fields.Str(dump_only=True)
    name = fields.Str(required=False)
    contact_email = fields.Email(required=False)
    phone_number = fields.Str()
    services_offered = fields.Str()


providers_bp = Blueprint(
    "Providers",
    "Providers",
    url_prefix="/api/v1/providers",
    description="This route is for service providers who organize events for seniors. It provides endpoints for them to manage their profiles and the events they have created. This is important for ensuring a steady stream of high-quality activities for seniors, making the platform a valuable resource for the community.",
)


@providers_bp.route("")
class ServiceProviderList(MethodView):
    @jwt_required()
    @roles_accepted("service_provider", "senior_citizen")
    @providers_bp.doc(
        summary="Get a list of all service providers.",
        description="This endpoint returns a list of all service providers, along with basic information about them. This allows users to see who is providing services in their community.",
    )
    @providers_bp.response(200, ServiceProviderSchema(many=True))
    def get(self):
        return ServiceProvider.query.all()

    @jwt_required()
    @roles_accepted("service_provider", "senior_citizen")
    @providers_bp.doc(
        summary="Create a new service provider profile.",
        description="This endpoint allows a new service provider to create a profile. The service provider must provide their name, contact information, and a description of the services they offer. This helps to build a network of trusted providers for seniors.",
    )
    @providers_bp.arguments(ServiceProviderSchema)
    @providers_bp.response(201, ServiceProviderSchema)
    def post(self, new_data):
        user_id = get_jwt_identity()
        provider = ServiceProvider(user_id=user_id, **new_data)
        db.session.add(provider)
        db.session.commit()
        return provider


@providers_bp.route("/<string:user_id>")
class ServiceProviderResource(MethodView):
    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(
        summary="Get information about a specific service provider.",
        description="This endpoint returns detailed information about a specific service provider, including their name, contact information, and the services they offer. This is useful for learning more about a provider before engaging with them.",
    )
    @providers_bp.response(200, ServiceProviderSchema)
    def get(self, user_id):
        return ServiceProvider.query.get_or_404(user_id)

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(
        summary="Update a service provider's information.",
        description="This endpoint allows a service provider to update their profile information. This is useful for keeping their contact information and service offerings up-to-date.",
    )
    @providers_bp.arguments(ServiceProviderSchema)
    @providers_bp.response(200, ServiceProviderSchema)
    def put(self, update_data, user_id):
        provider = ServiceProvider.query.get_or_404(user_id)
        for key, value in update_data.items():
            setattr(provider, key, value)
        db.session.commit()
        return provider

    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(
        summary="Delete a service provider's profile.",
        description="This endpoint allows a service provider to delete their profile. This is a permanent action and cannot be undone. This is useful for removing providers who are no longer active.",
    )
    @providers_bp.response(204)
    def delete(self, user_id):
        provider = ServiceProvider.query.get_or_404(user_id)
        db.session.delete(provider)
        db.session.commit()


@providers_bp.route("/<string:user_id>/events")
class ProviderEvents(MethodView):
    @jwt_required()
    @roles_accepted("service_provider")
    @providers_bp.doc(
        summary="Get all events for a specific service provider.",
        description="This endpoint returns a list of all events that have been created by a specific service provider. This is useful for seeing what activities a provider has organized in the past or has planned for the future.",
    )
    @providers_bp.response(200, EventSchema(many=True))
    def get(self, user_id):
        provider = ServiceProvider.query.get_or_404(user_id)
        return provider.events
