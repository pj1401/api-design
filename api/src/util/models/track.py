"""
Track helper classes.
module: src/util/models/track.py
"""

from enum import IntEnum
from api.src.util.models.base_db_model import BaseDbModel


class ModeEnum(IntEnum):
    minor = 0
    major = 1


class TrackModel(BaseDbModel):
    __tablename__: str = "tracks"
    track_id: str
    name: str
    duration_ms: int
    genre: str
    year: int
    tags: str
    total_playcount: int
    danceability: float
    mode: ModeEnum
    valence: float
    spotify_id: str
