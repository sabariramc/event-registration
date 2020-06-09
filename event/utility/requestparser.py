#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""

from functools import wraps
from datetime import datetime, date
from decimal import Decimal
import re

from flask import request

from .utility import is_non_empty_value
from ..exceptions import *


class ParamValidator:
    def __init__(self, query_param_definition=None, form_definition=None, json_definition=None, files_definition=None):
        self.query_param_definition = self.validate_type_definition(query_param_definition)
        self.form_definition = self.validate_type_definition(form_definition)
        self.json_definition = self.validate_type_definition(json_definition)
        self.files_definition = self.validate_type_definition(files_definition)

    def __call__(self, func_obj):
        @wraps(func_obj)
        def role_checker(*args, **kwargs):
            function_argument = {}
            if self.query_param_definition:
                function_argument.update(self.parser(request.args, self.query_param_definition))
            if self.form_definition:
                function_argument.update(self.parser(request.form, self.form_definition))
            if self.json_definition:
                function_argument.update(self.parser(request.json, self.json_definition))
            if self.files_definition:
                function_argument.update(self.parser(request.files, self.files_definition))
            kwargs.update(function_argument)
            return func_obj(*args, **kwargs)

        return role_checker

    @classmethod
    def parser(cls, params, definition, parent=None):
        validated_params = {}
        for key, type_def in definition.items():
            value = params.get(key)
            required = type_def.pop("required", False)
            try:
                print_key = f"{parent}.{key}" if parent else key
                if is_non_empty_value(value):
                    validated_params[key] = cls.parse_value(print_key, value, **type_def)
                elif required:
                    raise HTTPExceptionBadRequest(f"{print_key} should not be empty")
            finally:
                type_def["required"] = required
        return validated_params

    @classmethod
    def parse_value(cls, key, value, data_type, min_val=None, max_val=None, allowed_value_list=None, regex=None,
                    nested=False, sub_item_data_type=None, nested_data_definition=None):
        try:
            val = data_type(value)
        except Exception:
            raise HTTPExceptionBadRequest(f"{key} should be of type {data_type}")
        if nested:
            if sub_item_data_type:
                temp_list = []
                for item in val:
                    try:
                        list_item = sub_item_data_type(item)
                        temp_list.append(list_item)
                    except Exception:
                        raise HTTPExceptionBadRequest(f"{key} should be of {data_type} of {sub_item_data_type}")
                    cls.check_value_range(list_item, key, min_val, max_val, allowed_value_list, regex)
                val = temp_list
            elif nested_data_definition:
                if data_type is dict:
                    val = cls.parser(val, nested_data_definition, key)
                elif data_type is list:
                    temp_list = []
                    for item in val:
                        list_item = cls.parser(item, nested_data_definition, key)
                        temp_list.append(list_item)
                    val = temp_list
        else:
            cls.check_value_range(val, key, min_val, max_val, allowed_value_list, regex)
        return val

    @staticmethod
    def check_value_range(value, key, min_val=None, max_val=None, allowed_value_list=None, regex=None):
        if min_val and value < min_val:
            raise HTTPExceptionBadRequest(f"{key} should be greater than or equal to {min_val}")
        if max_val and value > max_val:
            raise HTTPExceptionBadRequest(f"{key} should be lesser than or equal to {max_val}")
        if allowed_value_list and value not in allowed_value_list:
            raise HTTPExceptionBadRequest(f"{key} should be one of these - {allowed_value_list}")
        if regex and re.search(regex, value) is None:
            raise HTTPExceptionBadRequest(f"{key} should be of format - {regex}")

    @staticmethod
    def validate_type_definition(type_definition):
        return type_definition


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
