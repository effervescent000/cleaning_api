import pytest
import tests.shapes as shapes


# POST endpoint tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.room_record_factory(label="Kitchen"),
            shapes.room_record_factory(label="Kitchen", user_id=2),
            "Return the created room.",
        )
    ],
)
def test_add_room(client, user_header, clean_room_record, given, expected, should):
    response = client.post("/rooms/", json=given, headers=user_header)
    assert response.status_code == 201

    data = response.json
    assert data["id"]

    assert clean_room_record(expected) == clean_room_record(data)
