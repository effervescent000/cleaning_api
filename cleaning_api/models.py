from . import db
from passlib.hash import pbkdf2_sha256 as hash


subtasks = db.Table(
    "subtasks",
    db.Column("parent_task_id", db.Integer, db.ForeignKey("tasks.id")),
    db.Column("child_task_id", db.Integer, db.ForeignKey("tasks.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(200))

    tasks = db.relationship(
        "Task", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    rooms = db.relationship(
        "Room", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    schedules = db.relationship(
        "Schedule", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    @staticmethod
    def hash_password(password):
        return hash.hash(password)

    def check_password(self, input):
        return hash.verify(input, self.password)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    # if the last_done date is null, it's assumed to be at 0% completed
    last_done = db.Column(db.DateTime)
    # period is measured in days
    period = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    tasks = db.relationship(
        "Task", backref="task", lazy=True, cascade="all, delete-orphan"
    )


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200))

    mon_points = db.Column(db.Integer, default=0)
    tue_points = db.Column(db.Integer, default=0)
    wed_points = db.Column(db.Integer, default=0)
    thu_points = db.Column(db.Integer, default=0)
    fri_points = db.Column(db.Integer, default=0)
    sat_points = db.Column(db.Integer, default=0)
    sun_points = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
