from implemented import auth_service
from flask import request, abort

def auth_required(func):
    def wrapper(*args, **kwargs):
        access_token = request.get_json()
        result = func(*args, **kwargs)
        Authorized = auth_service.check_access(access_token)
        if not Authorized:
            abort(401)
        else:
            return result
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        access_token = request.get_json()   
        Authorized = auth_service.check_access(access_token)
        admin = auth_service.check_admin(access_token)
        print(Authorized)
        print(admin)
        if not admin:
            abort(401)
        elif not Authorized:
            abort(401)
        result = func(*args, **kwargs)
        return result
    return wrapper