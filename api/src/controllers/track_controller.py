from flask import jsonify, request

from api.src.util.errors.application_error import (
    convert_to_http_error,
    log_original_error,
)


class TrackController:
    def __init__(self, track_service):
        self.track_service = track_service

    def get_tracks(self):
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            tracks = self.track_service.get()
            response = {"status": 200, "tracks": tracks}
            return jsonify(response), 200
        except Exception as err:
            log_original_error(err)
            http_err = convert_to_http_error(err)
            return jsonify(http_err.to_dict()), http_err.status
