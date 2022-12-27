from dao.users import UserDao

class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_users()

    def add_user(self, data):
        return self.dao.add_user(data)