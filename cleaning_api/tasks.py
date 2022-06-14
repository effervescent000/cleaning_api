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
@bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    query = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify(multi_task_schema.dump(query))


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
@bp.route("/<id>/", methods=["PUT"])
@jwt_required()
def update_task(id):
    if id == "None":
        return jsonify({"error": "invalid id"})
    data = request.get_json()
    task = Task.query.get(id)
    task.label = data.get("label", task.label)
    task.points = data.get("points", task.points)
    task.partial_effort = data.get("partial_effort", task.partial_effort)
    task.period = data.get("period", task.period)
    task.note = data.get("note", task.note)
    task.room_id = data.get("room_id", task.room_id)

    last_done = data.get("last_done", task.last_done)
    if last_done:
        task.last_done = arrow.get(data.get("last_done", task.last_done)).datetime
    else:
        task.last_done = None

    db.session.commit()
    return jsonify(one_task_schema.dump(task))


# DELETE endpoints


@bp.route("/<id>/", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    if id == "None":
        return jsonify({"error": "invalid id"}), 400
    task = Task.query.get(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        remaining = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify(multi_task_schema.dump(remaining))
    return jsonify({"error": "unauthorized"}), 401
