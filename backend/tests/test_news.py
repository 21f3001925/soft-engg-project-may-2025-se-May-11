from flask_smorest import abort


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestNewsAPI:

    def test_get_news_categories_ok(self, client, auth_headers):
        response = client.get("/api/v1/news/categories", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        # Optional: check some expected categories exist
        expected = {
            "business",
            "entertainment",
            "health",
            "science",
            "sports",
            "technology",
            "general",
        }
        assert expected.issubset(set(data["categories"]))

    def test_get_news_categories_unauthorized(self, client):
        # No auth header
        response = client.get("/api/v1/news/categories")
        assert response.status_code == 401

    def test_get_news_categories_forbidden(self, client, provider_auth_headers):
        # Provider is not allowed for news endpoints
        response = client.get("/api/v1/news/categories", headers=provider_auth_headers)
        assert response.status_code == 403

    def test_get_headlines_ok(self, client, auth_headers):
        response = client.get("/api/v1/news/", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert "articles" in data
        assert isinstance(data["articles"], list)
        # totalResults should be an int
        assert "totalResults" in data and isinstance(data["totalResults"], int)

    def test_get_headlines_with_category_filter(self, client, auth_headers):
        response = client.get("/api/v1/news/?category=health", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert isinstance(data["articles"], list)

    def test_get_headlines_with_query(self, client, auth_headers):
        response = client.get("/api/v1/news/?q=diabetes", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert isinstance(data["articles"], list)

    def test_get_headlines_unauthorized(self, client):
        response = client.get("/api/v1/news/")
        assert response.status_code == 401

    def test_get_headlines_forbidden(self, client, provider_auth_headers):
        response = client.get("/api/v1/news/", headers=provider_auth_headers)
        assert response.status_code == 403

    def test_newsapi_down_handling(self, client, auth_headers, monkeypatch):
        # Simulate NewsAPI.org being unavailable: monkeypatch the backend's network call
        # You may need to adjust attribute path to match your backend's architecture
        # This example assumes the route calls some news module's function fetch_news()

        def fake_fetch_news(*args, **kwargs):
            abort(502, message="Failed to fetch news from NewsAPI.")

        monkeypatch.setattr("routes.news.fetch_news_from_api", fake_fetch_news)

        response = client.get("/api/v1/news/", headers=auth_headers)
        assert response.status_code == 502
        data = response.get_json()
        assert data.get("message") == "Failed to fetch news from NewsAPI."
