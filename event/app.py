from flask import Flask, send_from_directory, jsonify, url_for, current_app, Blueprint
import os
from mysql.connector.pooling import MySQLConnectionPool

from . import settings
from .dbhandler import teardown_request as db_connection_teardown_request
from .handler import api


class Event(Flask):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'template_folder': settings.STATIC_ASSETS_PATH,
            'static_folder': settings.STATIC_ASSETS_PATH,
            'static_url_path': '',
        })
        super(Event, self).__init__(__name__, *args, **kwargs)
        self.connection_pool = None

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


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def site_map():
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return jsonify(links)


def serve(path=""):
    if path != "" and os.path.exists(current_app.static_folder + '/' + path):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')


def create_app():
    app = Event()
    app.add_url_rule('/<path:path>', 'app_client', serve)
    app.add_url_rule('/', 'app_index', serve)
    app.add_url_rule('/site-map', 'site_map', site_map)
    app.create_connection_pool()
    app.teardown_appcontext(db_connection_teardown_request)
    bp = Blueprint("api", __name__)
    api.init_app(bp)
    app.register_blueprint(bp, url_prefix="/event/api")
    return app
