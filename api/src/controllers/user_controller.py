from flask import jsonify, request

from api.src.util.errors.application_error import convert_to_http_error
from api.src.util.models.user import UserArguments


class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            user = self.user_service.create_user(
                UserArguments(username, email, password)
            )
            response = {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "status": 201,
            }
            return jsonify(response), 201
        except Exception as err:
            http_err = convert_to_http_error(err)
            return jsonify({"error": str(http_err)}), http_err.status | 500
