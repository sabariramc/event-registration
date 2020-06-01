#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 31-May-2020
"""

from flask_restx import Model, fields, reqparse
from datetime import date

registration_list = Model(
    "Registration list"
    , {
        "registration_date": fields.Date(readOnly=True, description="Date of registration")
        , "reg_uuid": fields.String(readOnly=True, description="Registration Id")
        , "full_name": fields.String(readOnly=True, description="Name of the registrant")
        , "no_of_ticket": fields.Integer(readOnly=True, description="No. of ticked registered")
        , "registration_type": fields.String(readOnly=True, description="Registration type")
    }
)
registration_confirmation = Model(
    "Registration confirmation",
    {
        "reg_uuid": fields.String(readOnly=True, description="Registration Id")
    }
)

registration_creation = Model(
    "Registration Creation",
    {
        "full_name": fields.String(required=True, description="Name of the registrant")
        , "mobile_number": fields.String(required=True, description="Mobile number", pattern="[0-9]{10}")
        , "email_address": fields.String(required=True, description="Email Address", pattern="[a-z.]+@[a-z]+.[a-z]+")
        , "country_code": fields.String(required=False, description="Country code of mobile number",
                                        pattern="+[0-9]{1,4}")
        , "no_of_ticket": fields.Integer(required=True, description="No. of ticked registered")
        , "registration_type": fields.String(required=True, description="Registration type")
    }
)

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('registration_date', type=date, required=False, help='Registration date')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')
