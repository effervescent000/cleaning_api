from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
    get_jwt,
    unset_jwt_cookies,
    jwt_required,
    current_user,
)

from .models import User
from .schema import UserSchema
from . import db, jwt

bp = Blueprint("auth", __name__, url_prefix="/auth")
one_user_schema = UserSchema()
multi_user_schema = UserSchema(many=True)


# GET endpoints


@bp.route("/check/", methods=["GET"])
@jwt_required(optional=True)
def check_for_logged_in_user():
    if current_user:
        return jsonify(one_user_schema.dump(current_user))
    return jsonify({})


# POST endpoints


@bp.route("/signup/", methods=["POST"])
def create_user():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username and password:
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=User.hash_password(password))
            db.session.add(new_user)
            db.session.commit()

            return generate_valid_user_response(new_user), 201
    return jsonify({"error": "invalid input"}), 400


@bp.route("/login/", methods=["POST"])
def login_user():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                return generate_valid_user_response(user)
    return jsonify({"error": "invalid input"}), 400


# utils


def generate_valid_user_response(user):
    response = jsonify(one_user_schema.dump(user))
    access_token = create_access_token(identity=user)
    set_access_cookies(response, access_token)
    return response


@current_app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(
                identity=User.query.filter_by(username=get_jwt_identity()).first()
            )
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).first()
