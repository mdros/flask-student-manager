import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_flask_app
from extensions.database import db


@pytest.fixture(scope="module")
def app():
    app = create_flask_app("config.TestConfig")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
