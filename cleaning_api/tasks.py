from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
import arrow

from .models import Task
from .schema import TaskSchema
from . import db

bp = Blueprint("tasks", __name__, url_prefix="/tasks")
one_task_schema = TaskSchema()
multi_task_schema = TaskSchema(many=True)

# GET endpoints

# POST endpoints
@bp.route("/", methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    label = data.get("label")
    if not label:
        return jsonify({"error": "no task label specified"}), 400
    points = data.get("points")
    if not points:
        return jsonify({"error": "no points specified"}), 400
    partial_effort = data.get("partial_effort", False)
    last_done = data.get("last_done")
    if last_done:
        last_done = arrow.get(last_done).datetime
    period = data.get("period")
    if not period:
        return jsonify({"error": "no period specified"}), 400
    note = data.get("note")
    room_id = data.get("room_id")
    if not room_id:
        return jsonify({"error": "no room ID specified"}), 400

    task = Task(
        label=label,
        points=points,
        partial_effort=partial_effort,
        last_done=last_done,
        period=period,
        note=note,
        room_id=room_id,
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(one_task_schema.dump(task)), 201


# PUT endpoints

# DELETE endpoints
