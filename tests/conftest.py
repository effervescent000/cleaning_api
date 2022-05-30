from dataclasses import dataclass
import pytest
from flask_jwt_extended import create_access_token

import tests.shapes as shapes
from cleaning_api import create_app, db
from cleaning_api.models import User

TEST_DATABASE_URI = "sqlite:///test_database.sqlite"


@pytest.fixture
def app():
    settings_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "dev",
        "JWT_HEADER_TYPE": "Bearer",
        "JWT_BLACKLIST_ENABLED": False,
        "JWT_TOKEN_LOCATION": ["headers"],
    }

    app = create_app(settings_override)

    with app.app_context():
        db.init_app(app)
        from cleaning_api.models import User, Task, Room, Schedule

        db.create_all()

        populate_test_data()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_header():
    return {
        "Authorization": f"Bearer {create_access_token(identity=User.query.filter_by(username='Admin').first())}"
    }


@pytest.fixture
def user_header():
    return {
        "Authorization": f"Bearer {create_access_token(identity=User.query.filter_by(username='testUser').first())}"
    }


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def populate_test_data():
    ...
