from . import ma


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "label", "room_id", "user_id")


multi_task_schema = TaskSchema(many=True)


class RoomSchema(ma.Schema):
    class Meta:
        fields = ("id", "label", "user_id", "tasks")

    tasks = multi_task_schema


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "role")
