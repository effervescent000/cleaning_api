from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Room
from .schema import RoomSchema
from . import db

bp = Blueprint("rooms", __name__, url_prefix="/rooms")
one_room_schema = RoomSchema()
multi_room_schema = RoomSchema(many=True)

# GET endpoints


@bp.route("/", methods=["GET"])
@jwt_required()
def get_all_rooms():
    query = Room.query.filter_by(user_id=current_user.id).all()
    return jsonify(multi_room_schema.dump(query))


# POST endpoints


@bp.route("/", methods=["POST"])
@jwt_required()
def add_room():
    data = request.get_json()
    type = data.get("type")
    if not type:
        return jsonify({"error": "no room type specified"}), 400

    label = data.get("label")
    if not label:
        label = type.title()

    room = Room(type=type, label=label, user_id=current_user.id)
    db.session.add(room)
    db.session.commit()
    return jsonify(one_room_schema.dump(room)), 201


# PUT endpoints


@bp.route("/<id>/", methods=["PUT"])
@jwt_required()
def update_room(id):
    if id == "None":
        return jsonify({"error": "invalid id"}), 400
    data = request.get_json()
    room = Room.query.get(id)
    room.type = data.get("type", room.type)
    room.label = data.get("label", room.type.title())
    db.session.commit()
    return jsonify(one_room_schema.dump(room))


# DELETE endpoints

# utils
