"""
The TrackService class.
"""


class TrackService:
    def __init__(self, track_repo):
        self.track_repo = track_repo

    def get(self):
        """Get all documents."""
        try:
            return self.track_repo.get()
        except Exception as err:
            raise err
