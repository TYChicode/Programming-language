from models.Storage import Storage

GRADE_FILE = "data/grades.txt"

# 成績管理
class GradeManager:
    def __init__(self):
        self.storage = Storage(GRADE_FILE)
    
    # 儲存成績
    def save_grade(self, teacher, student_name, subject, score):
        self.storage.save_record([teacher, student_name, subject, score])

    # 載入成績
    def load_grades(self, teacher_filter=None):
        grades = []
        for record in self.storage.load_records():
            if len(record) == 4:
                t, s, subj, score = record
                if teacher_filter is None or t == teacher_filter:
                    grades.append((t, s, subj, score))
        return grades