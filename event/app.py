from flask import Flask, send_from_directory, jsonify, url_for, g, current_app
import os
from mysql.connector.pooling import MySQLConnectionPool

from . import settings
from .model import teardown_request as db_connection_teardown_request


class Event(Flask):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'template_folder': settings.STATIC_ASSETS_PATH,
            'static_folder': settings.STATIC_ASSETS_PATH,
            'static_url_path': '',
        })
        super(Event, self).__init__(__name__, *args, **kwargs)
        self.connection_pool = {}

    def create_connection_pool(self, prefix="mysql", **connect_args):
        self.connection_pool = MySQLConnectionPool(
            pool_name=prefix,
            pool_reset_session=True,
            pool_size=10,
            **connect_args
        )

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
    return app
