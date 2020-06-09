#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""

from functools import wraps
from datetime import datetime, date
from decimal import Decimal

from flask import request

from .utility import is_non_empty_value
from ..exceptions import *


class ParamValidator:
    def __init__(self, query_param_definition=None, form_definition=None, json_definition=None, files_definition=None):
        self.query_param_definition = query_param_definition
        self.form_definition = form_definition
        self.json_definition = json_definition
        self.files_definition = files_definition

    def __call__(self, func_obj):
        @wraps(func_obj)
        def role_checker(*args, **kwargs):
            function_argument = {"self": args[0]}
            if self.query_param_definition:
                function_argument.update(self.parser(request.args, self.query_param_definition))
            if self.form_definition:
                function_argument.update(self.parser(request.form, self.form_definition))
            if self.json_definition:
                function_argument.update(self.parser(request.json, self.json_definition))
            if self.files_definition:
                function_argument.update(self.parser(request.files, self.files_definition))
            return func_obj(**function_argument)

        return role_checker

    @staticmethod
    def parser(request_data, definition):
        validated_params = {}
        for key, type_def in definition.items():
            value = request_data.get(key)
            type_name = type_def.get("name")
            required = type_def.get("required")
            regex = type_def.get("regex")
            if is_non_empty_value(value):
                try:
                    val = type_name(value)
                except Exception:
                    raise HTTPExceptionBadRequest(f"{key} should be of type {type_name}")
                min_val = type_def.get("min")
                max_val = type_def.get("max")
                value_list = type_def.get("list")
                if min_val and val < min_val:
                    raise HTTPExceptionBadRequest(f"{key} should be greater than or equal to {min_val}")
                if max_val and val > max_val:
                    raise HTTPExceptionBadRequest(f"{key} should be lesser than or equal to {max_val}")
                if value_list and val not in value_list:
                    raise HTTPExceptionBadRequest(
                        f"{key} not in the valid value, list of allowed values - {value_list}")
                if regex:
                    pass
                validated_params[key] = val
            elif required:
                raise HTTPExceptionBadRequest(f"{key} should not be empty")

        return validated_params


def parse_request(query_param_definition=None, form_definition=None, json_definition=None, files_definition=None):
    def inner_get_fu(fu):
        return ParamValidator(query_param_definition, form_definition, json_definition, files_definition)(fu)

    return inner_get_fu


def parse_args(query_param_definition):
    def inner_get_fu(fu):
        return parse_request(query_param_definition=query_param_definition)(fu)

    return inner_get_fu


def parse_form(form_definition):
    def inner_get_fu(fu):
        return parse_request(form_definition=form_definition)(fu)

    return inner_get_fu


def parse_json(json_definition):
    def inner_get_fu(fu):
        return parse_request(json_definition=json_definition)(fu)

    return inner_get_fu


def parse_file(files_definition):
    def inner_get_fu(fu):
        return parse_request(files_definition=files_definition)(fu)

    return inner_get_fu


class BaseParam:
    def __init__(self, data_type):
        self.data_type = data_type

    def __repr__(self):
        return str(self.data_type)


class DateParam(BaseParam):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=date)

    def __call__(self, value):
        return datetime.strptime(value, self.fmt_string).date()

    def __repr__(self):
        return f"{str(self.data_type)} and format {self.fmt_string}"


class DecimalParam(BaseParam):
    def __init__(self):
        super().__init__(data_type=Decimal)

    def __call__(self, value):
        return Decimal(str(value))


class FileParam(BaseParam):
    def __init__(self, mimetype=None):
        self.mimetype = mimetype
        super().__init__(data_type="File Stream")

    def __call__(self, value):
        if self.mimetype:
            file_mime_type = value.mimetype
            if file_mime_type.startswith(self.mimetype) is False:
                raise Exception()
        return value

    def __repr__(self):
        if self.mimetype:
            return f"{str(self.data_type)} and file type should be '{self.mimetype}'"
        super(FileParam, self).__repr__()
