import pytest
from flask_jwt_extended import create_access_token
import arrow

import tests.shapes as shapes
from cleaning_api import create_app, db
from cleaning_api.models import User, Room, Task

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
        "Authorization": f"Bearer {create_access_token(identity=User.query.filter_by(username='TestUser').first())}"
    }


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def clean_room_record():
    def inner(record):
        record.pop("id", None)
        record.pop("tasks", None)
        return record

    return inner


@pytest.fixture
def clean_task_record():
    def inner(record):
        record.pop("id", None)
        return record

    return inner


def populate_test_data():
    def clean_dates_in_factory(record):
        return {**record, "last_done": arrow.get(record["last_done"]).datetime}

    users = [
        User(**shapes.user_record_factory(id=1, username="Admin", role="admin")),
        User(**shapes.user_record_factory(id=2, username="TestUser")),
    ]

    for user in users:
        user.password = User.hash_password("test_password")
        db.session.add(user)
        db.session.commit()

    rooms = [
        shapes.room_record_factory(
            id=1, type="bedroom", label="Bedroom", user_id=users[0].id
        ),
        shapes.room_record_factory(
            id=2, type="bathroom", label="Bathroom", user_id=users[0].id
        ),
        shapes.room_record_factory(
            id=3, type="bedroom", label="Bedroom", user_id=users[1].id
        ),
        shapes.room_record_factory(
            id=4, label="Bathroom", type="bathroom", user_id=users[1].id
        ),
    ]

    for room in rooms:
        db.session.add(Room(**room))
        db.session.commit()

    USER_ONE = users[0]
    USER_ONE_BEDROOM = USER_ONE.rooms[0]
    USER_ONE_BATHROOM = USER_ONE.rooms[1]

    USER_TWO = users[1]
    USER_TWO_BEDROOM = USER_TWO.rooms[0]
    USER_TWO_BATHROOM = USER_TWO.rooms[1]

    tasks = [
        shapes.task_record_factory(
            id=1,
            label="Clean clothes up",
            room_id=USER_ONE_BEDROOM.id,
            user_id=users[0].id,
        ),
        shapes.task_record_factory(
            id=2, label="Vacuum", room_id=USER_ONE_BEDROOM.id, user_id=users[0].id
        ),
        shapes.task_record_factory(
            id=3,
            label="Clean mirror",
            room_id=USER_ONE_BATHROOM.id,
            user_id=users[0].id,
        ),
        shapes.task_record_factory(
            id=4,
            label="Wash bath mat",
            room_id=USER_ONE_BATHROOM.id,
            user_id=users[0].id,
        ),
        shapes.task_record_factory(
            id=5,
            label="Dust surfaces",
            room_id=USER_TWO_BEDROOM.id,
            user_id=users[1].id,
        ),
        shapes.task_record_factory(
            id=6,
            label="Vacuum",
            room_id=USER_TWO_BEDROOM.id,
            user_id=users[1].id,
        ),
        shapes.task_record_factory(
            id=7,
            label="Dust surfaces",
            room_id=USER_TWO_BATHROOM.id,
            user_id=users[1].id,
        ),
        shapes.task_record_factory(
            id=8, label="Clean sink", room_id=USER_TWO_BATHROOM.id, user_id=users[1].id
        ),
    ]

    for task in tasks:
        db.session.add(Task(**clean_dates_in_factory(task)))
        db.session.commit()
