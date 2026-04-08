"""
Defines track routes.
"""

from flask import Blueprint, g
from api.src.controllers.tracks_controller import TracksController
from api.src.util.errors.application_error import HttpError

tracks_bp = Blueprint("tracks", __name__)


@tracks_bp.before_request
def before_request():
    """Create objects once per request."""
    g.tracks_controller = TracksController()


@tracks_bp.route("/", methods=["GET"])
def get_tracks():
    return g.tracks_controller.get_tracks()
