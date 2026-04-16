"""
Track helper classes.
module: src/util/models/track.py
"""

from enum import IntEnum

from pydantic import BaseModel


class ModeEnum(IntEnum):
    minor = 0
    major = 1


class TrackRow(BaseModel):
    track_id: str
    track_name: str
    duration_ms: int
    genre: str
    year: int
    tags: str
    total_playcount: int
    danceability: float
    mode: ModeEnum
    valence: float
    spotify_id: str
