#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from flask_restx import Resource


class RegistrationList(Resource):

    def get(self):
        return ""


class Registration(Resource):

    def get(self, user_id):
        return ""
