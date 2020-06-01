#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 30-May-2020
"""

from flask_restx import Api

from .admin import Admin
from .registration import *

api = Api(version='1.0', title='API',
          description='API for event registration')
admin_ns = api.namespace(name="Admin API", path="/admin")
api.add_namespace(registration_ns, path="/registration")

admin_ns.add_resource(Admin, "")

registration_ns.add_resource(RegistrationList, "")
registration_ns.add_resource(Registration, "/<int:user_id>")
