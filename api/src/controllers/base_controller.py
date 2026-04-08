"""
The BaseController class.
"""

from flask import jsonify, request

from api.src.services.base_service import BaseService
from api.src.util.errors.application_error import (
    convert_to_http_error,
    log_original_error,
)


class BaseController:
    def __init__(self, service: BaseService):
        self.service = service

    def get(self):
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            fetched = self.service.get(limit)
            response = {"status": 200, "fetched": fetched}
            return jsonify(response), 200
        except Exception as err:
            log_original_error(err)
            http_err = convert_to_http_error(err)
            return jsonify(http_err.to_dict()), http_err.status
