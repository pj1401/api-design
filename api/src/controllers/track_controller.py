"""
The TrackController class.
"""

from api.src.controllers.base_controller import BaseController


class TrackController(BaseController):
    def __init__(self, track_service):
        super().__init__(track_service)
