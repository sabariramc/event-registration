from flask import Flask
import os
from mysql.connector.pooling import MySQLConnectionPool

from . import settings
from .dbhandler import teardown_request as db_connection_teardown_request
from .handler import *


class Event(Flask):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'template_folder': settings.STATIC_ASSETS_PATH,
            'static_folder': settings.STATIC_ASSETS_PATH,
            'static_url_path': '',
        })
        super(Event, self).__init__(__name__, *args, **kwargs)
        self.connection_pool = None
        self.dynamic_asset_path = None

    def create_connection_pool(self):
        pool_config = {
            "host": settings.EVENT_MYSQL_DATABASE_HOST,
            "port": settings.EVENT_MYSQL_DATABASE_PORT,
            "database": settings.EVENT_MYSQL_DATABASE_NAME,
            "user": settings.EVENT_MYSQL_DATABASE_USER,
            "password": settings.EVENT_MYSQL_DATABASE_PASSWORD,
            "charset": settings.EVENT_MYSQL_DATABASE_CHARSET,
            "use_unicode": True,
            "get_warnings": True,
            "ssl_verify_cert": False,
            "pool_name": self.__class__.__name__,
            "pool_reset_session": settings.EVENT_MYSQL_DATABASE_POOL_RESET_SESSION,
            "pool_size": settings.EVENT_MYSQL_DATABASE_POOL_SIZE
        }
        if settings.EVENT_MYSQL_DATABASE_SSL_VERIFY_CERT:
            pool_config["ssl_verify_cert"] = True
            pool_config["ssl_ca"] = settings.EVENT_MYSQL_DATABASE_SSL_CA_PATH
        self.connection_pool = MySQLConnectionPool(**pool_config)

    # def __del__(self):
    #     try:
    #         self.connection_pool._remove_connections()
    #     except Exception:
    #         pass
    #     super(Event, self).__del__()


def create_app():
    app = Event()
    app.config["SERVER_NAME"] = settings.EVENT_FLASK_SERVER
    app.dynamic_asset_path = settings.EVENT_ASSET_MEDIA_FOLDER
    if os.path.isdir(app.dynamic_asset_path) is False:
        os.makedirs(app.dynamic_asset_path)
    app.create_connection_pool()
    app.teardown_appcontext(db_connection_teardown_request)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(helper_blueprint)
    return app
