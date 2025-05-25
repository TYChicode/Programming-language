from models.Storage import Storage

STUDENT_FILE = "data/students.txt"

# 學生管理
class StudentManager:
    def __init__(self):
        self.storage = Storage(STUDENT_FILE)

    # 儲存學生資料
    def save_student(self, *fields):
        self.storage.save_record(fields)

    # 載入學生資料
    def load_students(self):
        students = []
        for record in self.storage.load_records():
            students.append(tuple(record))
        return students
    
    # 學生查看自己個人資料
    def get_student_by_account(self, account):
        for record in self.storage.load_records():
            if len(record) >= 2 and record[0] == account:
                return {
                    "account": record[0],
                    "name": record[1],
                }
        return None