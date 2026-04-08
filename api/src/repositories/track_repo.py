"""
The TrackRepository class.
"""

from api.src.repositories.base_repo import BaseRepository


class TrackRepository(BaseRepository):
    def __init__(self, db_manager):
        super().__init__(db_manager, "tracks")
