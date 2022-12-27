from dao.auth import AuthDao
import jwt
from flask import abort
import datetime,calendar
from constants import secret,algo

class AuthService:
    def __init__(self, dao : AuthDao):
        self.dao = dao
    
    def check_user(self, user_data):
        AuthID = self.dao.check_user(user_data)
        if AuthID:
            tokens = self.generate_jwt(user_data)
            self.dao.change_tokens(AuthID, tokens)
            return (tokens)
        else:
            abort(401)
        
    def check_key(self, refresh_key):
        user_data = self.dao.check_key(refresh_key)
        if user_data:
            tokens = self.generate_jwt(user_data)
            self.dao.change_tokens(user_data, tokens)
            return (tokens)
        else:
            abort(401)

    def check_access(self, access_key):
        try:
            access_key = access_key.get("access_token")
        except:
            return False
        Authorized = self.dao.check_access(access_key)
        if Authorized:
            return True
        return False

    def check_admin(self, access_key):
        return self.dao.check_admin(access_key)
        

    def generate_jwt(self, user_data):
        try:
            data = {
                "username" : user_data.get('username'),
                "role" : user_data.get('role')
            }
        except:
            data = {
                "username" : user_data.username,
                "role" : user_data.role
            }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret ,algorithm = algo)
        min30 = datetime.datetime.utcnow() + datetime.timedelta(days= 130)
        data["exp"] = calendar.timegm(min30.timetuple())
        refresh_token = jwt.encode(data, secret ,algorithm = algo)
        
        return {'access_token':access_token, 'refresh_token':refresh_token}