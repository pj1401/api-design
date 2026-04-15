"""
The TrackController class.
module: src/controllers/track_controller.py
"""

from api.src.controllers.base_controller import BaseController
from api.src.services.track_service import TrackService


class TrackController(BaseController[TrackService]):
    def __init__(self, track_service: TrackService):
        super().__init__(track_service)
