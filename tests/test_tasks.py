import pytest
import tests.shapes as shapes

# GET endpoint tests
def test_get_all_tasks(client, user_header):
    response = client.get("/tasks/", headers=user_header)
    assert response.status_code == 200

    data = response.json
    assert len(data) == 4


# POST endpoint tests
@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.task_record_factory(room_id=3),
            shapes.task_record_factory(room_id=3, user_id=2),
            "Return the passed in task.",
        )
    ],
)
def test_add_task(client, user_header, clean_task_record, given, expected, should):
    response = client.post("/tasks/", json=given, headers=user_header)
    assert response.status_code == 201

    data = response.json
    assert data["id"]
    assert clean_task_record(expected) == clean_task_record(data)


# PUT endpoint tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            shapes.task_record_factory(
                room_id=3, id=5, user_id=2, label="Clean mirror"
            ),
            shapes.task_record_factory(
                room_id=3, id=5, user_id=2, label="Clean mirror"
            ),
            "Modify the specified task when inputs are valid.",
        ),
        (
            shapes.task_record_factory(room_id=3, user_id=2, label="Clean mirror"),
            {"error": "invalid id"},
            "Return error when no ID is included.",
        ),
        (
            {"id": 5, "label": "Clean mirror"},
            shapes.task_record_factory(
                room_id=3, id=5, user_id=2, label="Clean mirror"
            ),
            "Modify only specified fields.",
        ),
        (
            {"id": 5, "last_done": None},
            shapes.task_record_factory(
                room_id=3, id=5, label="Dust surfaces", user_id=2, last_done="None"
            ),
            "Allow None as a valid last_done value.",
        ),
    ],
)
def test_update_task(client, user_header, given, expected, should):
    response = client.put(f"/tasks/{given['id']}/", json=given, headers=user_header)
    assert response.status_code == 200

    data = response.json
    assert expected == data


# DELETE endpoint tests


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            {"id": 5},
            [
                shapes.task_record_factory(
                    id=6,
                    label="Vacuum",
                    room_id=3,
                    user_id=2,
                ),
                shapes.task_record_factory(
                    id=7,
                    label="Dust surfaces",
                    room_id=4,
                    user_id=2,
                ),
                shapes.task_record_factory(
                    id=8, label="Clean sink", room_id=4, user_id=2
                ),
            ],
            "Return user's remaining tasks when one is deleted.",
        )
    ],
)
def test_delete_room_valid(client, user_header, given, expected, should):
    response = client.delete(f"/tasks/{given['id']}/", headers=user_header)

    data = response.json
    assert expected == data


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            {"id": 5},
            {"error": "unauthorized"},
            "Return an error if a user tries to delete another user's record.",
        )
    ],
)
def test_delete_room_invalid(client, admin_header, given, expected, should):
    response = client.delete(f"/tasks/{given['id']}/", headers=admin_header)

    data = response.json
    assert expected == data
