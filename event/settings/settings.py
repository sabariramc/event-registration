import os

from .helper import fix_assets_path

STATIC_ASSETS_PATH = fix_assets_path(os.environ.get(
    "EVENT_FIXED_ASSET_PATH", "../client/build"))
