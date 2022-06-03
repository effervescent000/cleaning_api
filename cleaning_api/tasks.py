from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Task
from .schema import TaskSchema
from . import db

bp = Blueprint("tasks", __name__, url_prefix="/tasks")
one_task_schema = TaskSchema()
multi_task_schema = TaskSchema(many=True)

# GET endpoints

# POST endpoints

# PUT endpoints

# DELETE endpoints
