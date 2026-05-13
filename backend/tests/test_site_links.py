import pytest
from fastapi.testclient import TestClient

from home.app import app
from home.controllers.dependencies import public_cache
from home.core.database import Base, engine, init_db
from home.services.auth_service import auth_service


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    public_cache.clear()
    auth_service._sessions.clear()
    init_db()
    yield
    public_cache.clear()
    auth_service._sessions.clear()


def test_public_site_links_seeded():
    with TestClient(app) as client:
        response = client.get("/pub/site-links")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"][0]["name"] == "博客"


def test_admin_site_links_require_login():
    with TestClient(app) as client:
        response = client.get("/cms/site-links")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 401


def test_login_and_replace_site_links():
    with TestClient(app) as client:
        login = client.post(
            "/oms/auth/login",
            data={"username": "admin", "password": "admin123"},
        )
        assert login.json()["code"] == 200

        save = client.post(
            "/cms/site-links",
            json=[
                {
                    "icon": "Blog",
                    "name": "新博客",
                    "link": "https://example.com",
                    "enabledFlag": 1,
                }
            ],
        )

        assert save.json() == {"code": 200, "msg": "success", "data": True}
        public = client.get("/pub/site-links").json()

    assert public["data"][0]["name"] == "新博客"
