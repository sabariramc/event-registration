#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 06-Jun-2020
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
        jsonEncoder = json.JSONEncoder()
        return jsonEncoder.default(obj)
