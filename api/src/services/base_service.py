"""
The BaseService class.
module: src/services/base_service.py
"""

from typing import Generic, TypeVar
from api.src.repositories.base_repo import BaseRepository

TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseService(Generic[TRepository]):
    def __init__(self, repository: TRepository):
        self.repository = repository

    def get(self, limit: int):
        """Get all documents."""
        try:
            return self.repository.get(limit)
        except Exception as err:
            raise err
