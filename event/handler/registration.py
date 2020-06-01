#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from flask import request
from flask_restx import Resource, Namespace

from ..dbhandler import execute_sql_statement
from .sqlqueries import *
from .requestmodel import *

registration_ns = Namespace("Registration")
registration_ns.add_model("Registration list", registration_list)
registration_ns.add_model("Registration confirmation", registration_confirmation)


class RegistrationList(Resource):

    @registration_ns.response(200, "Registration list", registration_list)
    @registration_ns.expect(pagination_arguments)
    def get(self):
        filter_condition = []
        filter_params = {}
        query_params = request.query_string
        sql = sql_get_registration_list.format(" AND ".join(filter_condition))
        return execute_sql_statement(sql, parameters=filter_params)

    @registration_ns.response(201, "Registration success", registration_confirmation)
    def post(self):
        form_data = request.form
        id_data = request.files.get("file")
        file_data = id_data.read()
        print(form_data)
        return ""


class Registration(Resource):

    def get(self, user_id):
        return ""
