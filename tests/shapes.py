from typing import Union
from random import randint
from cleaning_api.models import User, Task, Room, Schedule

factory_dict = dict[str, Union[str, int]]


def user_record_factory(
    id: int, *, username: str = None, role: str = None
) -> factory_dict:
    return {"id": id, "username": username or f"abcd-{id}", "role": role}


def task_record_factory(
    *, id: int = None, label: str = None, room_id: int, user_id: int = None
) -> factory_dict:
    return {
        "id": id or randint(1, 100000),
        "label": label or f"Task {id}",
        "room_id": room_id,
        "user_id": user_id,
    }


def room_record_factory(
    *, id: int = None, label: str = None, user_id: int = None
) -> factory_dict:
    return {
        "id": id or randint(1, 100000),
        "label": label or f"Room {id}",
        "user_id": user_id,
    }


def schedule_record_factory(
    id: int, *, points: dict = {}, user_id: int = None
) -> factory_dict:
    return {
        "id": id,
        "mon_points": points.get("mon", 0),
        "tue_points": points.get("tue", 0),
        "wed_points": points.get("wed", 0),
        "thu_points": points.get("thu", 0),
        "fri_points": points.get("fri", 0),
        "sat_points": points.get("sat", 0),
        "sun_points": points.get("sun", 0),
        "user_id": user_id,
    }
