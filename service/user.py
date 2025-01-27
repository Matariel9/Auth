from dao.users import UserDao

class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_users()

    def add_user(self, data):
        return self.dao.add_user(data)
    
    def get_user(self, bid):
        return self.dao.get_user(bid)
    
    def change_user(self, bid, data):
        return self.dao.change_user(bid, data)
    
    def delete_user(self, bid):
        return self.dao.delete_user()