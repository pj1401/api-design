"""
BaseDbModel class.
module: src/util/models/base_db_model.py
"""

from pydantic import BaseModel


class BaseDbModel(BaseModel):
    __tablename__: str
