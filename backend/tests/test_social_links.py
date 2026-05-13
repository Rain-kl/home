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


def test_public_social_links_seeded():
    with TestClient(app) as client:
        response = client.get("/pub/social-links")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"][0]["name"] == "Github"


def test_admin_social_links_require_login():
    with TestClient(app) as client:
        response = client.get("/cms/social-links")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 401


def test_login_and_replace_social_links():
    with TestClient(app) as client:
        login = client.post(
            "/oms/auth/login",
            data={"username": "admin", "password": "admin123"},
        )
        assert login.json()["code"] == 200

        save = client.post(
            "/cms/social-links",
            json=[
                {
                    "name": "GitHub",
                    "icon": "/images/icon/github.png",
                    "tip": "看看代码",
                    "url": "https://github.com/example",
                    "enabledFlag": 1,
                }
            ],
        )

        assert save.json() == {"code": 200, "msg": "success", "data": True}
        public = client.get("/pub/social-links").json()

    assert public["data"][0]["name"] == "GitHub"
    assert public["data"][0]["tip"] == "看看代码"
