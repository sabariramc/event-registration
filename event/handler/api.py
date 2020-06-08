#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from flask_restful import Api
from flask import Blueprint
from .registration import *
from ..exceptions import HTTPException


class EventAPI(Api):

    def handle_error(self, e):
        if isinstance(e, HTTPException):
            return {"message": e.message}, e.code
        else:
            return super().handle_error(e)


api = EventAPI()
api.add_resource(RegistrationList, "/registration")
api.add_resource(Registration, "/registration/<user_id>")
api.add_resource(RegistrationType, "/registration/config")

bp = Blueprint("api", __name__, url_prefix="/event/api")
api.init_app(bp)
