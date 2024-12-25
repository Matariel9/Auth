from implemented import auth_service
from flask import request, abort
import jwt

from constants import secret, algo

def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=algo)
        except Exception:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            decoded = jwt.decode(token, secret, algorithms=algo)
            if decoded.get("role") != "admin":
                abort(401)
        except Exception:
            abort(401)
        return func(*args, **kwargs)
    return wrapper