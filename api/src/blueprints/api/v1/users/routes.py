"""
Defines user routes.
"""

from flask import Blueprint, g
from api.src.controllers.user_controller import UserController
from api.src.repositories.user_repo import UserRepository
from api.src.services.user_service import UserService

users_bp = Blueprint("users", __name__)


@users_bp.before_request
def before_request():
    """Create objects once per request."""
    g.user_repo = UserRepository(g.db_manager)
    g.user_service = UserService(g.user_repo)
    g.user_controller = UserController(g.user_service)


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # TODO: Make get user?
    return g.user_controller.get_user(user_id)


@users_bp.route("/users/register", methods=["POST"])
def create_user():
    return g.user_controller.create_user()
