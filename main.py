import tkinter as tk
from tkinter import messagebox, simpledialog

import os
from rsa_utils import *
from models import UserManager, StudentManager, GradeManager

DATA_FILE = "data/users.txt"
STUDENT_FILE = "data/students.txt"
GRADE_FILE = "data/grades.txt"

# 載入或建立密鑰
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key)
else:
    private_key = load_private_key()
    public_key = load_public_key()

# 選擇身分介面
def show_dashboard_by_role(role, username, user_manager, student_manager, grade_manager, name):
    if role == "admin":
        show_admin_dashboard(student_manager)
    elif role == "teacher":
        show_teacher_dashboard(username, student_manager, grade_manager)
    elif role == "student":
        show_student_dashboard(username, name, grade_manager, student_manager)  
        
# 管理員後台  
def show_admin_dashboard(student_manager):
    dash = tk.Toplevel()
    dash.title("管理員後台")

    tk.Label(dash, text="管理員功能：").pack()
    tk.Button(dash, text="檢視學生列表", command=lambda: show_students_list(dash, student_manager)).pack()
    tk.Button(dash, text="關閉", command=dash.destroy).pack()

def show_students_list(parent, student_manager):
    win = tk.Toplevel(parent)
    win.title("所有學生")

    student_list = tk.Listbox(win, width=40)
    student_list.pack()
    for record in student_manager.load_students():
        account = record[0]
        name = record[1] if len(record) > 1 else ""
        student_list.insert(tk.END, f"{account} ({name})")


# 教師後台
def show_teacher_dashboard(username, student_manager, grade_manager):
    dash = tk.Toplevel()
    dash.title("教師後台")

    tk.Label(dash, text=f"教師 {username} 的功能：").pack(pady=5)
    
    tk.Button(dash, text="檢視學生列表", command=lambda: show_students_list(dash, student_manager)).pack(pady=3)

    def add_grade():
        student_name = simpledialog.askstring("學生姓名", "請輸入學生姓名：", parent=dash)
        subject = simpledialog.askstring("科目", "請輸入科目：", parent=dash)
        score = simpledialog.askinteger("分數", "請輸入分數：", parent=dash)
        if student_name and subject and score is not None:
            grade_manager.save_grade(username, student_name, subject, score)
            messagebox.showinfo("成功", "成績已新增")

    tk.Button(dash, text="新增學生成績", command=add_grade).pack(pady=3)

    def view_my_grades():
        grade_window = tk.Toplevel(dash)
        grade_window.title("已輸入的成績")
        tk.Label(grade_window, text=f"{username} 輸入的成績如下：").pack()
        listbox = tk.Listbox(grade_window, width=50)
        listbox.pack()
        for t, s, subj, score in grade_manager.load_grades(teacher_filter=username):
            listbox.insert(tk.END, f"{s} - {subj}: {score} 分")

    tk.Button(dash, text="查看已輸入的成績", command=view_my_grades).pack(pady=3)

    tk.Button(dash, text="關閉", command=dash.destroy).pack(pady=5)

# 學生後台
def show_student_dashboard(account, username, grade_manager, student_manager):
    dash = tk.Toplevel()
    dash.title("學生後台")

    tk.Label(dash, text=f"學生 {username} 的功能：").pack(pady=5)
    
    def view_personal_info():
        info = student_manager.get_student_by_account(account)
        if info:
            info_text = f"帳號：{info['account']}\n姓名：{info['name']}"
            messagebox.showinfo("個人資料", info_text)
        else:
            messagebox.showerror("錯誤", "找不到學生資料")

    def view_grades():
        grade_window = tk.Toplevel(dash)
        grade_window.title("成績查詢")
        tk.Label(grade_window, text=f"{username} 的成績如下：").pack()
        listbox = tk.Listbox(grade_window, width=50)
        listbox.pack()
        for t, s, subj, score in grade_manager.load_grades():
            if s == username:
                listbox.insert(tk.END, f"{t} - {subj}: {score} 分")

    tk.Button(dash, text="查看個人資料", command=view_personal_info).pack(pady=3)
    tk.Button(dash, text="查看成績", command=view_grades).pack(pady=3)
    tk.Button(dash, text="關閉", command=dash.destroy).pack(pady=5)

# 主介面
def show_main_window():
    root = tk.Tk()
    root.title("登入系統")

    tk.Label(root, text="帳號:").grid(row=0, column=0)
    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1)

    tk.Label(root, text="密碼:").grid(row=1, column=0)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.grid(row=1, column=1)

    tk.Label(root, text="身份:").grid(row=2, column=0)
    role_var = tk.StringVar(root)
    role_var.set("student")
    role_menu = tk.OptionMenu(root, role_var, "admin", "teacher", "student")
    role_menu.grid(row=2, column=1)

    name_label = tk.Label(root, text="姓名(學生專用):")
    name_entry = tk.Entry(root)

    def on_role_change(*args):
        if role_var.get() == "student":
            name_label.grid(row=3, column=0)
            name_entry.grid(row=3, column=1)
        else:
            name_label.grid_remove()
            name_entry.grid_remove()

    role_var.trace_add("write", lambda *args: on_role_change())
    on_role_change()

    user_manager = UserManager()
    student_manager = StudentManager()
    grade_manager = GradeManager()

    # 登入功能
    def login():
        username = entry_user.get()
        password = entry_pass.get()
        role, name = user_manager.check_login(username, password)
        if role:
            messagebox.showinfo("成功", f"登入成功，身份為：{role}")
            root.withdraw()
            show_dashboard_by_role(role, username, user_manager, student_manager, grade_manager, name)
        else:
            messagebox.showerror("失敗", "登入失敗")

    # 註冊功能
    def register():
        username = entry_user.get()
        password = entry_pass.get()
        role = role_var.get()
        name = name_entry.get() if role == "student" else ""
        if role not in ["admin", "teacher", "student"]:
            messagebox.showerror("錯誤", "請選擇身份")
            return
        if role == "student" and not name:
            messagebox.showerror("錯誤", "學生身份必須填寫姓名")
            return
        user_manager.save_user(username, password, role, name)
        if role == "student":
            student_manager.save_student(username, name)
        messagebox.showinfo("註冊成功", f"{role} 帳號已註冊")

    tk.Button(root, text="登入", command=login).grid(row=4, column=0)
    tk.Button(root, text="註冊", command=register).grid(row=4, column=1)

    root.mainloop()

if __name__ == "__main__":
    show_main_window()
