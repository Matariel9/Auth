from flask_restx import Namespace, Resource
from flask import request
from implemented import auth_service

auth_ns = Namespace('auth')

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        user_data = request.get_json()
        return auth_service.check_user(user_data)
    
    def put(self):
        refresh_key = request.get_json()
        return auth_service.check_key(refresh_key)
        