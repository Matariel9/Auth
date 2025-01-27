from dao.model.user import User, UserSchema
import datetime, calendar, jwt
from constants import secret, algo
import json


class UserDao:
    def __init__(self, session):
        self.session = session

    def get_users(self):
        all_users = self.session.query(User).all()
        users_schema = UserSchema(many = True)
        return users_schema.dump(all_users)

    def add_user(self, data):
        user_info = User(**data)

        user_hash = self.generate_jwt(data)

        self.session.add(user_hash)
        self.session.add(user_info)
        self.session.commit()
        self.session.close()
        return True

    def get_user(self, bid):
        user = self.session.query(User).filter(User.id == bid)
        return UserSchema().dump(*user.all())

    def change_user(self, bid, data):
        user = self.session.query(User).filter(User.id == bid).one()
        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")
        
        self.session.add(user)
        self.session.commit()
        return UserSchema().dump(user)

    def delete_user(self, bid):
        user = self.session.query(User).filter(User.id == bid)
        self.session.delete(user)
        self.session.commit()
        return 203

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
        