#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from datetime import date
from uuid import uuid4
import os

from flask import request, current_app
from flask_restful import Resource

from ..dbhandler import execute_sql_statement
from .sqlqueries import *


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

    def post(self):
        registration_type_map = current_app.enums.REGISTRATION_TYPE._asdict()
        file = request.files.get("id_card")
        file_mime_type = file.mimetype
        if file_mime_type.startswith("image") is False:
            return "Id card should be a image", 403
        form_data = request.form
        insert_data = {
            "full_name": form_data.get("full_name")
            , "mobile_number": form_data.get("mobile_number")
            , "email_address": form_data.get("email_address")
            , "registration_type": registration_type_map.get(form_data.get("registration_type")).value
            , "no_of_ticket": form_data.get("no_of_ticket")
            , "registration_date": date.today()
        }
        de_dup_check = execute_sql_statement(sql_check_registration, parameters=insert_data)[0].get("cnt")
        if de_dup_check:
            return "Mobile number/ email address already in use", 409
        insert_data["reg_uuid"] = uuid4().hex
        file_ext = file.filename.split(".")[-1]
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], insert_data.get("reg_uuid"))
        os.mkdir(path)
        file_name = f"id_card.{file_ext}"
        path = os.path.join(path, file_name)
        file.save(path)
        insert_data["id_card_path"] = os.path.join(insert_data["reg_uuid"], file_name)
        execute_sql_statement(sql_create_registration, parameters=insert_data, is_insert=True)
        return {
            "registration_id": insert_data["reg_uuid"]
        }


class RegistrationType(Resource):

    def get(self):
        return current_app.registration_type


class Registration(Resource):

    def get(self, user_id):
        data = execute_sql_statement(sql_get_registration, parameters={"reg_uuid": user_id})
        if data:
            return data[0]
        else:
            return "Not Found", 404
