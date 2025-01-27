from dao.model.user import User
from flask import abort
import jwt
from constants import secret, algo
import hmac
import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

class AuthDao:
    def __init__(self, session):
        self.session = session

    def check_user(self, user_data):
        print(user_data.get('username'))
        try:
            users = self.session.query(User).filter(User.username == user_data.get('username')).all()
            if users == []:
                return False
        except:
            return False
        passw = user_data.get('password')
        
        # passw = self.get_hash(user_data.get('password'))
        for user in users:
            if passw == user.password:
                print(user.role)
                return user
        return False
        # return hmac.compare_digest(passw, user[0].password)
    
    def check_key(self, refresh_key): 
        # try:
        #     user_auth = self.session.query(Auth).filter(Auth.refresh_token == data.get('refresh_key')).one()
        #     if not user_auth:
        #         print("11")
        #         return False
        # except:
        #     return False
        
        
        try:
            token = refresh_key['refresh_token'].split("Bearer ")[-1]
            decoded = jwt.decode(token, secret, algorithms=algo)
        except Exception:
            abort(401)
        
        print(decoded)
        return decoded

    def get_hash(self, password):
            return hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),  # Convert the password to bytes
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ).decode("utf-8", "ignore")