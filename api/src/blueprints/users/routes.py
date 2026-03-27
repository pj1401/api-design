from flask import Blueprint, request, g
import flask
from api.src.controllers.user_controller import UserController
from api.src.repositories.user_repo import UserRepository
from api.src.services.user_service import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<int:user_id>', methods=['GET'])

@users_bp.route('/users', methods=['POST'])
def create_user():
    user_controller = UserController(UserService(UserRepository(g.db_manager)))
    return user_controller.create_user()
