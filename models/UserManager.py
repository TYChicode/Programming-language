from models.Storage import Storage

DATA_FILE = "data/users.txt"

# 使用者管理
class UserManager:
    def __init__(self):
        self.storage = Storage(DATA_FILE)

    def save_user(self, username, password, role, name=""):
        self.storage.save_record([username, password, role, name])

    def check_login(self, username, password):
        for record in self.storage.load_records():
            if len(record) == 4:
                u, p, r, n = record
                if u == username and p == password:
                    return r, n  
        return None, None
    
    def load_all_users(self):
        users = []
        for record in self.storage.load_records():
            if len(record) >= 3:
                users.append((record[0], record[2], record[3] if len(record) > 3 else ""))
        return users

    def update_user(self, account, new_password, new_name=""):
        records = self.storage.load_records()
        updated = []
        for r in records:
            if r[0] == account:
                r[1] = new_password
                if new_name:
                    if len(r) > 3:
                        r[3] = new_name
                    elif len(r) == 3:
                        r.append(new_name)
            updated.append(r)
        self.storage.save_all_records(updated)

    def delete_user(self, account):
        records = self.storage.load_records()
        updated = [r for r in records if r[0] != account]
        self.storage.save_all_records(updated)
        
    def view_user_info(self, account):
        records = self.storage.load_records()
        for r in records:
            if r[0] == account:
                role = r[2] if len(r) > 2 else ""
                name = r[3] if len(r) > 3 else ""
                info = f"帳號: {account}\n身份: {role}\n姓名: {name}"
                # 用 tkinter 顯示視窗
                import tkinter.messagebox as messagebox
                messagebox.showinfo("使用者資訊", info)
                return
        # 找不到帳號
        import tkinter.messagebox as messagebox
        messagebox.showerror("錯誤", f"找不到帳號 {account}")
