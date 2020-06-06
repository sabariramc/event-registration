from flask import Flask
import os
from mysql.connector.pooling import MySQLConnectionPool
from collections import defaultdict, namedtuple

from . import settings
from .dbhandler import teardown_request as db_connection_teardown_request
from .dbhandler import execute_sql_statement
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
        self.enums = None

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
            "pool_size": settings.EVENT_MYSQL_DATABASE_POOL_SIZE,
            "autocommit": True
        }
        if settings.EVENT_MYSQL_DATABASE_SSL_VERIFY_CERT:
            pool_config["ssl_verify_cert"] = True
            pool_config["ssl_ca"] = settings.EVENT_MYSQL_DATABASE_SSL_CA_PATH
        self.connection_pool = MySQLConnectionPool(**pool_config)

    def load_enums(self):
        sql = 'SELECT * FROM c_enum'
        cnx = self.connection_pool.get_connection()
        enum_list = execute_sql_statement(sql, sql_cnx=cnx)
        enum_map = defaultdict(list)
        enum_obj_map = {}
        for enum in enum_list:
            enum_map[enum.get("enum_type_name")].append(enum)
        value_tuple = namedtuple("VALUE", ["value", "name"])
        for enum_name_code, enum_value_list in enum_map.items():
            value_map = {
                enum_value.get("enum_code"): value_tuple(enum_value.get("enum_value"), enum_value.get("enum_name"))
                for enum_value in enum_value_list
            }
            temp_named_tuple = namedtuple(enum_name_code, list(value_map.keys()))
            enum_obj_map[enum_name_code.upper()] = temp_named_tuple(**value_map)
        enum_type_tuple = namedtuple("ENUM", enum_obj_map.keys())
        self.enums = enum_type_tuple(**enum_obj_map)
        cnx.close()
    # def __del__(self):
    #     try:
    #         self.connection_pool._remove_connections()
    #     except Exception:
    #         pass
    #     super(Event, self).__del__()


def create_app():
    app = Event()
    app.config.from_pyfile("settings/config.py")
    if os.path.isdir(app.config["UPLOAD_FOLDER"]) is False:
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.create_connection_pool()
    app.load_enums()
    app.teardown_appcontext(db_connection_teardown_request)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(helper_blueprint)
    return app
