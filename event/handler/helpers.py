#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 06-Jun-2020
"""

from flask import Blueprint, current_app, url_for, jsonify, send_from_directory
import os


bp = Blueprint("helper", __name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@bp.route("/site-map", methods=["GET"])
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


@bp.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)



@bp.route("/<path:path>")
@bp.route("/")
def ui_host(path=""):
    if path != "" and os.path.exists(current_app.static_folder + '/' + path):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')
