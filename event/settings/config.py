#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 06-Jun-2020
"""

import os
from event.settings.helper import fix_assets_path
from event.utility import json_serializer

SERVER_NAME = os.environ.get("FLASK_SERVER_NAME", None)
UPLOAD_FOLDER = os.environ.get("EVENT_ASSET_MEDIA_FOLDER", fix_assets_path("../dynamic_asset"))
TEMP_FOLDER = os.environ.get("EVENT_ASSET_TEMP_FOLDER", fix_assets_path("../temp_asset"))
RESTFUL_JSON = {"default": json_serializer}
