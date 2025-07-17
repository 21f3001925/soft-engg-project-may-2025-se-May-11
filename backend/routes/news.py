from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import current_app, jsonify
from marshmallow import Schema, fields, validate
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted
import requests
import logging

# type: ignore


NEWSAPI_CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]


class NewsQuerySchema(Schema):
    q = fields.Str(required=False, description="Search query")
    category = fields.Str(
        required=False,
        description="News category (optional)",
        validate=validate.OneOf(NEWSAPI_CATEGORIES),
    )


class NewsResponseSchema(Schema):
    status = fields.Str()
    totalResults = fields.Int()
    articles = fields.List(fields.Dict())
    message = fields.Str(required=False)


news_bp = Blueprint(
    "news",
    "news",
    url_prefix="/api/v1/news",
    description="Fetch news from NewsAPI.org.",
)


@news_bp.route("/categories")
@jwt_required()
@roles_accepted("caregiver", "senior_citizen")
def get_categories():
    """Return the list of available news categories."""
    return jsonify({"categories": NEWSAPI_CATEGORIES})


def fetch_news_from_api(params: dict) -> dict:
    """Helper to fetch news from NewsAPI.org and handle errors."""
    url = "https://newsapi.org/v2/top-headlines"
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"NewsAPI request failed: {e}")
        abort(502, message="Failed to fetch news from NewsAPI.")
    return {}


@news_bp.route("/")
class NewsResource(MethodView):
    """Resource for fetching news articles from NewsAPI.org."""

    @jwt_required()
    @roles_accepted("caregiver", "senior_citizen")
    @news_bp.arguments(NewsQuerySchema, location="query")
    @news_bp.response(200, NewsResponseSchema)
    def get(self, args):
        """Get top headlines from NewsAPI.org."""
        api_key = current_app.config.get("NEWSAPI_KEY")
        if not api_key:
            abort(500, message="News API key not configured.")
        params = {"apiKey": api_key, "language": "en"}
        if args.get("q"):
            params["q"] = args["q"]
        if args.get("category"):
            params["category"] = args["category"]
        return fetch_news_from_api(params)
