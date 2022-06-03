import pytest
import tests.shapes as shapes

# GET endpoint tests

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

# DELETE endpoint tests
