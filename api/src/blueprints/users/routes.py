from flask import Blueprint, request, g

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return g.user_controller.get_user(user_id)

@users_bp.route('/users', methods=['POST'])
def create_user():
    return g.user_controller.create_user()
