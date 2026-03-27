from flask import Blueprint, request
from api.src.controllers.user_controller import UserController
from flask_injector import inject

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@inject
def get_user(user_controller: UserController, user_id: int):
    return user_controller.get_user(user_id)

@users_bp.route('/users', methods=['POST'])
@inject
def create_user(user_controller: UserController):
    return user_controller.create_user()
