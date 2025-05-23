from models.Storage import Storage

DATA_FILE = "data/users.txt"

# 使用者管理
class UserManager:
    def __init__(self):
        self.storage = Storage(DATA_FILE)

    def save_user(self, username, password, role, name=""):
        # name 只有學生用，老師和管理員可空白
        self.storage.save_record([username, password, role, name])

    def check_login(self, username, password):
        for record in self.storage.load_records():
            if len(record) == 4:
                u, p, r, n = record
                if u == username and p == password:
                    return r, n  
        return None, None