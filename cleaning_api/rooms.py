from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Room
from .schema import RoomSchema
from . import db

bp = Blueprint("rooms", __name__, url_prefix="/rooms")
one_room_schema = RoomSchema()
multi_room_schema = RoomSchema(many=True)

# GET endpoints

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

# DELETE endpoints

# utils
