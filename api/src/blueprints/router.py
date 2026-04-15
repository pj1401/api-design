"""
The main router that registers the api routes.
module: src/blueprints/router.py
"""

from flask import Blueprint, jsonify
from api.src.blueprints.api.v1.router import router_v1_bp
from api.src.util.errors.application_error import HttpError

router_bp = Blueprint("/", __name__)
router_bp.register_blueprint(router_v1_bp, url_prefix="/api/v1")


@router_bp.errorhandler(404)
def not_found(err: Exception):
    http_err = HttpError(err, 404, "The requested resource was not found.")
    return jsonify(http_err.to_dict()), http_err.status
