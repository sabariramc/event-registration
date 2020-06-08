#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""

from functools import wraps
from .utility import is_non_empty_value
from datetime import datetime, date
from decimal import Decimal


class ParamValidator:
    def __init__(self, param_definition):
        if isinstance(param_definition, dict) is False:
            raise Exception("Definition Error")
        self.param_definition = param_definition

    def __call__(self, func_obj):
        @wraps(func_obj)
        def role_checker(*args, **kwargs):
            validation_param = args[1]
            query_params = self.validate(validation_param)
            query_params["self"] = args[0]
            return func_obj(**query_params)

        return role_checker

    def validate(self, params):
        validated_params = {}
        for key, type_def in self.param_definition.items():
            value = params.get(key)
            type_name = type_def.get("name")
            required = type_def.get("required")
            if is_non_empty_value(value):
                try:
                    val = type_name(value)
                except Exception:
                    raise KNABHTTPExceptionBadRequest(f"{key} should be of type {type_name}")
                min_val = type_def.get("min")
                max_val = type_def.get("max")
                value_list = type_def.get("list")
                if min_val and val < min_val:
                    raise KNABHTTPExceptionBadRequest(f"{key} should be greater than or equal to {min_val}")
                if max_val and val > max_val:
                    raise KNABHTTPExceptionBadRequest(f"{key} should be lesser than or equal to {max_val}")
                if value_list and val not in value_list:
                    raise KNABHTTPExceptionBadRequest(
                        f"{key} not in the valid value, list of allowed values - {value_list}")
                validated_params[key] = val
            elif required:
                raise KNABHTTPExceptionBadRequest(f"{key} should not be empty")

        return validated_params


def validate_params(param_definition):
    def inner_get_fu(fu):
        return ParamValidator(param_definition)(fu)

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
