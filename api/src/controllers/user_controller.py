"""
The UserController class.
module: src/controllers/user_controller.py
"""

from flask import jsonify, request
from flask_jwt_extended import create_access_token
from api.src.controllers.base_controller import BaseController
from api.src.services.user_service import UserService
from api.src.util.errors.application_error import (
    convert_to_http_error,
    log_original_error,
)
from api.src.util.models.user import UserLogin, UserArguments


class UserController(BaseController[UserService]):
    def __init__(self, user_service: UserService):
        super().__init__(user_service, "users")

    def create_user(self):
        try:
            data = request.get_json()
            user_arguments = UserArguments(**data)
            user = self.service.create_user(user_arguments)
            response: dict[str, int | str] = {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "status": 201,
            }
            return jsonify(response), 201
        except Exception as err:
            log_original_error(err)
            http_err = convert_to_http_error(err)
            return jsonify(http_err.to_dict()), http_err.status

    def login(self):
        try:
            data = request.get_json()
            user_login = UserLogin(**data)
            user = self.service.login(user_login)
            access_token: str = create_access_token(
                identity={
                    "user_id": user.user_id,
                    "username": user.username,
                    "permission_level": user.permission_level,
                }
            )
            response: dict[str, int | str] = {
                "access_token": access_token,
                "status": 200,
            }
            return jsonify(response), 200
        except Exception as err:
            log_original_error(err)
            http_err = convert_to_http_error(err)
            return jsonify(http_err.to_dict()), http_err.status
