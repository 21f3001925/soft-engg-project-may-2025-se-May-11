from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app, jsonify
from marshmallow import Schema, fields
import requests

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
    language = fields.Str(missing="en", description="Language code (default: en)")
    q = fields.Str(required=False, description="Search query")
    category = fields.Str(required=False, description="News category (optional)")


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
def get_categories():
    """Return the list of available news categories."""
    return jsonify({"categories": NEWSAPI_CATEGORIES})


@news_bp.route("/")
class NewsResource(MethodView):
    @news_bp.arguments(NewsQuerySchema, location="query")
    @news_bp.response(200, NewsResponseSchema)
    def get(self, args):
        api_key = current_app.config.get("NEWSAPI_KEY")
        if not api_key:
            return {
                "status": "error",
                "totalResults": 0,
                "articles": [],
                "message": "News API key not configured.",
            }, 500
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": api_key, "language": args.get("language", "en")}
        if args.get("q"):
            params["q"] = args["q"]
        if args.get("category"):
            params["category"] = args["category"]
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            return {
                "status": "error",
                "totalResults": 0,
                "articles": [],
                "message": str(e),
            }, 502
