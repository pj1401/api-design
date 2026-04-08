"""
Defines track routes.
"""

from flask import Blueprint, g
from api.src.controllers.track_controller import TrackController
from api.src.repositories.track_repo import TrackRepository
from api.src.services.track_service import TrackService
from api.src.util.errors.application_error import HttpError

tracks_bp = Blueprint("tracks", __name__)


@tracks_bp.before_request
def before_request():
    """Create objects once per request."""
    g.track_repo = TrackRepository(g.db_manager)
    g.track_service = TrackService(g.track_repo)
    g.track_controller = TrackController(g.track_service)


@tracks_bp.route("/", methods=["GET"])
def get_tracks():
    return g.track_controller.get_tracks()
