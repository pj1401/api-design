"""
The BaseController class.
module: src/controllers/base_controller.py
"""

from typing import Any, Generic, TypeVar
from flask import jsonify, request
from api.src.services.base_service import BaseService
from api.src.util.errors.application_error import (
    convert_to_http_error,
    log_original_error,
)

TService = TypeVar("TService", bound=BaseService[Any])


class BaseController(Generic[TService]):
    def __init__(self, service: TService):
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
