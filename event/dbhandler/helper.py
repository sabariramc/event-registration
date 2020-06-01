#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 31-May-2020
"""

import json
from datetime import datetime, date
from decimal import Decimal


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime) or isinstance(obj, date):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, object):
        return str(obj)
    else:
        json_encoder = json.JSONEncoder()
        return json_encoder.default(obj)


def get_json_serialized_obj(obj):
    """
    Provide json compatible object
    :param obj: dict/list object
    :return: json compatible object
    """
    return json.loads(json.dumps(obj, default=json_serializer))
