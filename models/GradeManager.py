from models.Storage import Storage

GRADE_FILE = "data/grades.txt"

# 成績管理
class GradeManager:
    def __init__(self):
        self.storage = Storage(GRADE_FILE)
    
    # 儲存成績
    def save_grade(self, teacher, student_account, subject, score):
        self.storage.save_record([teacher, student_account, subject, score])

    # 載入成績
    def load_grades(self, teacher_filter=None):
        grades = []
        for record in self.storage.load_records():
            if len(record) == 4:
                t, s, subj, score = record
                if teacher_filter is None or t == teacher_filter:
                    grades.append((t, s, subj, score))
        return grades
    
    # 更新成績
    def update_grade(self, teacher, student_account, subject, new_score):
        
        updated = False
        updated_records = []
        for record in self.storage.load_records():
            if len(record) == 4:
                t, s, subj, score = record                
                if t == teacher and s == student_account and subj == subject:
                    updated_records.append([t, s, subj, new_score])
                    updated = True
                else:
                    updated_records.append(record)
        if updated:
            self.storage.save_all_records(updated_records)
        return updated

    # 刪除成績
    def delete_grade(self, teacher, student_account, subject):
        
        deleted = False
        updated_records = []
        for record in self.storage.load_records():
            if len(record) == 4:
                t, s, subj, score = record
                if t == teacher and s == student_account and subj == subject:
                    deleted = True
                else:
                    updated_records.append(record)
        if deleted:
            self.storage.save_all_records(updated_records)
        return deleted