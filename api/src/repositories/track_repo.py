"""
The TrackRepository class.
module: src/repositories/track_repo.py
"""

from api.src.db.connection_manager import DatabaseConnectionManager
from api.src.repositories.base_repo import BaseRepository


class TrackRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseConnectionManager):
        super().__init__(db_manager, "tracks")
