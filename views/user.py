from flask_restx import Namespace, Resource
from flask import request
from implemented import user_service
from decorators import auth_required, admin_required

user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        return user_service.get_all()

    def post(self):
        data = request.get_json()
        return user_service.add_user(data)

@user_ns.route('/<int:bid>')
class UserView(Resource):
    @auth_required
    def get(self, bid):
        return user_service.get_user(bid)
    
    @auth_required
    def put(self, bid):
        data = request.json
        return user_service.change_user(bid, data)

    @admin_required
    def delete(self, bid):
        return user_service.delete_user(bid)