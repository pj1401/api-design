"""
The BaseRepository class.
"""


class BaseRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get(self):
        try:
            conn = self.db_manager.get_connection()
            return {"track1": "Name of track"}
        except Exception as err:
            raise err
