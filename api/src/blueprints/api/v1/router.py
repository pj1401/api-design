"""
API version 1 router. Registers API endpoints.
"""

from flask import Blueprint
from api.src.blueprints.api.v1.users.routes import users_bp
from api.src.blueprints.api.v1.tracks.routes import tracks_bp

router_v1_bp = Blueprint("/", __name__)
router_v1_bp.register_blueprint(users_bp, url_prefix="/users")
router_v1_bp.register_blueprint(tracks_bp, url_prefix="/tracks")
