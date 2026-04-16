"""
The BaseService class.
module: src/services/base_service.py
"""

from typing import Any, Generic, TypeVar
from api.src.repositories.base_repo import BaseRepository

TRepository = TypeVar("TRepository", bound=BaseRepository[Any])


class BaseService(Generic[TRepository]):
    def __init__(self, repository: TRepository):
        self.repository = repository

    def get(self, limit: int):
        """Get all documents."""
        try:
            fetched = self.repository.get(limit)
            return [row.__dict__ for row in fetched]
        except Exception as err:
            raise err
