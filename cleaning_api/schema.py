from . import ma


class TaskSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "label",
            "points",
            "last_done",
            "period",
            "note",
            "room_id",
            "user_id",
        )


multi_task_schema = TaskSchema(many=True)


class RoomSchema(ma.Schema):
    class Meta:
        fields = ("id", "label", "type", "user_id", "tasks")

    tasks = ma.Nested(multi_task_schema)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "role")
