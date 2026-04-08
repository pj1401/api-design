"""
The BaseService class.
"""

from api.src.repositories.base_repo import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get(self):
        """Get all documents."""
        try:
            return self.repository.get()
        except Exception as err:
            raise err
