from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Room
from .schema import RoomSchema
from . import db, jwt

bp = Blueprint("room", __name__, url_prefix="/room")
one_room_schema = RoomSchema()
multi_room_schema = RoomSchema(many=True)

# GET endpoints

# POST endpoints

# PUT endpoints

# DELETE endpoints

# utils
