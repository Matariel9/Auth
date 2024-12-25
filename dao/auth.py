from dao.model.user import User
from dao.model.auth import Auth
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
        

    
    def check_key(self, data): 
        try:
            user_auth = self.session.query(Auth).filter(Auth.refresh_token == data.get('refresh_key')).one()
            if not user_auth:
                print("11")
                return False
        except:
            return False
        
        return self.session.query(User).filter(User.id == user_auth.userid).one()

    def check_access(self, access_key):
        try:
            print(access_key)
            users_auth = self.session.query(Auth).filter(Auth.access_token == access_key).one()
            if(users_auth):
                return True
            else:
                return False
        except:
            return False

    def check_admin(self, access_key):
        try:
            users_auth = self.session.query(Auth).filter(Auth.access_token == access_key['access_token']).one()
            user = self.session.query(User).filter(users_auth.userid == User.id).one()
            if(user.role == 'admin'):
                return True
            else:
                return False
        except:
            return False

    def change_tokens(self, __user__, tokens):
        return tokens

    def get_hash(self, password):
            return hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),  # Convert the password to bytes
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ).decode("utf-8", "ignore")