from flask_restx import Namespace, Resource
from flask import request
from implemented import user_service

user_ns = Namespace('users')

@user_ns.route('/')
class UserView(Resource):
    def get(self):
        return user_service.get_all()

    def post(self):
        data = request.get_json()
        return user_service.add_user(data)