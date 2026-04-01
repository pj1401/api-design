from flask import jsonify, request

from api.src.util.errors.application_error import convert_to_http_error
from api.src.util.models.user import UserArguments


class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self):
        try:
            data = request.get_json()
            user_arguments = UserArguments(**data)
            user = self.user_service.create_user(user_arguments)
            response = {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "status": 201,
            }
            return jsonify(response), 201
        except Exception as err:
            http_err = convert_to_http_error(err)
            return jsonify(http_err.to_dict()), http_err.status
