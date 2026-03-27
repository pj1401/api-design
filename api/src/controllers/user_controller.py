from flask import jsonify

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self):
        #TODO: Add some arguments
        user = self.user_service.create_user()
        if user:
            return jsonify(user)
        return jsonify({"error": "An error occurred when creating user"}), 400
