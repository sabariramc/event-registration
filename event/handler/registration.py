#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from flask import request
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
        file_data = id_data.read()
        print(form_data)
        return ""


class Registration(Resource):

    def get(self, user_id):
        return ""
