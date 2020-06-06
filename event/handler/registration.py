#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

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
        form_data = request.form
        id_data = request.files.get("file")
        full_name = form_data.get("full_name")
        mobile_number = form_data.get("mobile_number")
        email_address = form_data.get("email_address")
        registration_type_code = form_data.get("registration_type")
        no_of_tickets = form_data.get("n_of_types")
        print(form_data)
        return ""


class RegistrationType(Resource):

    def get(self):
        return current_app.registration_type


class Registration(Resource):

    def get(self, user_id):
        return ""
