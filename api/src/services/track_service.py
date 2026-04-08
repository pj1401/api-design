"""
The TrackService class.
"""

from api.src.services.base_service import BaseService


class TrackService(BaseService):
    def __init__(self, track_repo):
        super().__init__(track_repo)
