#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from datetime import date
from uuid import uuid4
import os
import shutil
from time import sleep

from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename

from ..dbhandler import execute_sql_statement
from .sqlqueries import *
from ..exceptions import *
from ..utility import *

from ..constants import REGISTRATION_TYPE_LIST


def map_temp_file(temp_file_name):
    file_name = secure_filename(temp_file_name)
    current_path = os.path.join(current_app.config['TEMP_FOLDER'], file_name)
    if not os.path.isfile(current_path):
        return False, 'File not found'
    return True, current_path


class RegistrationList(Resource):

    def get(self):
        filter_condition = []
        filter_params = {}
        query_params = request.args
        page_no = int(query_params.get("page_no", 1))
        per_page = int(query_params.get("per_page", 10))
        sql = sql_get_registration_list % " AND ".join(filter_condition)
        count = execute_sql_statement(sql_count_wrapper % sql, parameters=filter_params)[0].get("cnt")
        sql = f"{sql} LIMIT {per_page} OFFSET {(page_no - 1) * per_page}"
        return {
            "count": count
            , "data": execute_sql_statement(sql, parameters=filter_params)
        }

    @parse_request_json({
        "name": {"data_type": str, "required": True, 'regex': r"^[a-zA-Z_']+$"}
        , "mobile_number": {"data_type": str, "required": True, 'regex': r'^[0-9]{10}$',
                            'regex_error_message': 'should be 10 digits'}
        , "email_address": {"data_type": str, "required": True,
                            "regex": r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$"}
        , "registration_type": {"data_type": str, "required": True, 'allowed_value_list': REGISTRATION_TYPE_LIST}
        , "no_of_ticket": {"data_type": int, "required": True, 'min_val': 1}
        , "id_card_file": {"data_type": str, "required": True, 'validator': map_temp_file}
    })
    def post(self, id_card_file, name, mobile_number, email_address, no_of_ticket, registration_type):
        registration_type_map = current_app.enums.REGISTRATION_TYPE._asdict()
        insert_data = {
            "full_name": name
            , "mobile_number": mobile_number
            , "email_address": email_address
            , "registration_type": registration_type_map.get(registration_type).value
            , "no_of_ticket": no_of_ticket
            , "registration_date": date.today()
        }
        de_dup_check = execute_sql_statement(sql_check_registration, parameters=insert_data)[0].get("cnt")
        if de_dup_check:
            raise HTTPExceptionConflict("Mobile number/ email address already in use")
        insert_data["reg_uuid"] = uuid4().hex
        file_ext = id_card_file.split(".")[-1]
        file_name = f"id_card.{file_ext}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], insert_data.get("reg_uuid"))
        os.mkdir(path)
        destination_path = os.path.join(path, file_name)
        shutil.move(id_card_file, destination_path)
        insert_data["id_card_path"] = os.path.join(insert_data["reg_uuid"], file_name)
        execute_sql_statement(sql_create_registration, parameters=insert_data, is_insert=True)
        return {
            "registration_id": insert_data["reg_uuid"]
        }


class RegistrationType(Resource):

    def get(self):
        sleep(10)
        registration_type = current_app.enums.REGISTRATION_TYPE._asdict()
        return [{"key": key, "value": value[1]} for key, value in registration_type.items()]


class Registration(Resource):

    def get(self, user_id):
        data = execute_sql_statement(sql_get_registration, parameters={"reg_uuid": user_id})
        if data:
            return data[0]
        else:
            return "Not Found", 404
