"""
The TrackService class.
module: src/services/track_service.py
"""

from api.src.repositories.track_repo import TrackRepository
from api.src.services.base_service import BaseService


class TrackService(BaseService):
    def __init__(self, track_repo: TrackRepository):
        super().__init__(track_repo)
