"""
Defines track routes.
"""

from flask import Blueprint, g, jsonify
from api.src.util.errors.application_error import HttpError

tracks_bp = Blueprint("tracks", __name__)


@tracks_bp.route("/", methods=["GET"])
def get_tracks():
    return jsonify({"status": 501, "message": "Not Implemented"}), 501
