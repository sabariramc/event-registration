#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from uuid import uuid4
from time import time


from flask_restful import Api
from flask import Blueprint, jsonify, request, send_from_directory
from .registration import * 
from ..exceptions import HTTPException


class EventAPI(Api):

    def handle_error(self, e):
        if isinstance(e, HTTPException):
            return {"message": e.message}, e.code
        else:
            return super().handle_error(e)


api = EventAPI()
api.add_resource(RegistrationList, "/registration")
api.add_resource(Registration, "/registration/<user_id>")
api.add_resource(RegistrationType, "/registration/config")

bp = Blueprint("api", __name__, url_prefix="/event/api")
api.init_app(bp)


@bp.route("/upload", methods=["POST"])
def upload_file():
    content_type = request.content_type
    allowed_mime_type = ['image/png', 'image/jpg', 'image/jpeg']
    if content_type not in allowed_mime_type:
        return 'Image should be of type PNG, JPG, JPEG', 400
    extension_map = {
        'image/png': 'png'
        , 'image/jpg': 'jpg'
        , 'image/jpeg': 'jpeg'
    }
    file_name = f"{int(time())}_{uuid4().hex}.{extension_map.get(content_type)}"
    path = os.path.join(current_app.config['TEMP_FOLDER'], file_name)
    with open(path, 'wb') as fp:
        fp.write(request.data)
    return jsonify({"upload_file": file_name})


@bp.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route("/preview/download/<path:filename>", methods=["GET"])
def get_temp_file(filename):
    return send_from_directory(current_app.config['TEMP_FOLDER'], filename)
