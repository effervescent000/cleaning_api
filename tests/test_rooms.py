import pytest
import tests.shapes as shapes

# GET endpoint tests
def test_get_all_rooms(client, user_header):
    response = client.get("/rooms/", headers=user_header)
    assert response.status_code == 200

    data = response.json
    assert len(data) == 2


# POST endpoint tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.room_record_factory(label="Kitchen", type="kitchen"),
            shapes.room_record_factory(label="Kitchen", type="kitchen", user_id=2),
            "Return the created room when room type and label are both new.",
        ),
        (
            shapes.room_record_factory(type="bedroom"),
            shapes.room_record_factory(label="Bedroom", type="bedroom", user_id=2),
            "Return the created room when room type and label are both pre-existing.",
        ),
    ],
)
def test_add_room_valid(
    client, user_header, clean_room_record, given, expected, should
):
    response = client.post("/rooms/", json=given, headers=user_header)
    assert response.status_code == 201

    data = response.json
    assert data["id"]

    assert clean_room_record(expected) == clean_room_record(data)


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.room_record_factory(),
            {"error": "no room type specified"},
            "Return an error when no type is specified.",
        ),
    ],
)
def test_add_room_invalid(client, user_header, given, expected, should):
    response = client.post("/rooms/", json=given, headers=user_header)
    assert response.status_code == 400

    data = response.json
    assert expected == data
