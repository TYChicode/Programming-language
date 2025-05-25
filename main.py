import tkinter as tk
from tkinter import messagebox, simpledialog
from models import UserManager, StudentManager, GradeManager


DATA_FILE = "data/users.txt"
STUDENT_FILE = "data/students.txt"
GRADE_FILE = "data/grades.txt"

# 通用視窗設定函式
def configure_window(window, title="視窗"):
    window.title(title)
    window.geometry("500x400")
    window.resizable(False, False)

# 選擇身分介面
def show_dashboard_by_role(role, username, user_manager, student_manager, grade_manager, name):
    if role == "admin":
        show_admin_dashboard(user_manager, student_manager)
    elif role == "teacher":
        show_teacher_dashboard(username, student_manager, grade_manager)
    elif role == "student":
        show_student_dashboard(username, name, grade_manager, student_manager)  

# 管理員後台  
def show_admin_dashboard(user_manager, student_manager):
    dash = tk.Toplevel()
    configure_window(dash, "管理員後台")

    tk.Label(dash, text="管理員功能：").pack()
    tk.Button(dash, text="管理所有帳號", command=lambda: manage_all_users(dash, user_manager)).pack()
    tk.Button(dash, text="關閉", command=dash.destroy).pack()

def manage_all_users(parent, user_manager):
    win = tk.Toplevel(parent)
    configure_window(win, "帳號管理")

    all_users = user_manager.load_all_users()

    grouped = {"admin": [], "teacher": [], "student": []}
    for u in all_users:
        grouped[u[1]].append(u)
    for role in grouped:
        grouped[role].sort(key=lambda x: x[0])

    for role, users in grouped.items():
        tk.Label(win, text=f"== {role.upper()} ==", font=("Arial", 10, "bold")).pack()
        for account, r, name in users:
            frame = tk.Frame(win)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=f"{account} ({name})").pack(side="left")
            tk.Button(frame, text="修改", command=lambda acc=account: edit_user(acc, user_manager)).pack(side="right")
            tk.Button(frame, text="刪除", command=lambda acc=account: delete_user(acc, user_manager, win)).pack(side="right")

def edit_user(account, user_manager):
    new_pass = simpledialog.askstring("修改密碼", f"輸入 {account} 的新密碼：")
    new_name = simpledialog.askstring("修改姓名", f"輸入 {account} 的新姓名（可留空）：")
    if new_pass:
        user_manager.update_user(account, new_pass, new_name)
        messagebox.showinfo("成功", f"{account} 資料已更新")
    else:
        messagebox.showerror("錯誤", "請重新輸入")

def delete_user(account, user_manager, parent_window):
    confirm = messagebox.askyesno("確認刪除", f"確定要刪除 {account}？")
    if confirm:
        user_manager.delete_user(account)
        messagebox.showinfo("成功", f"{account} 已刪除")
        parent_window.destroy() 
        manage_all_users(parent_window.master, user_manager)

# 教師後台
def show_teacher_dashboard(username, student_manager, grade_manager):
    dash = tk.Toplevel()
    configure_window(dash, "教師後台")

    tk.Label(dash, text=f"教師 {username} 的功能：").pack(pady=5)

    def show_students_list(parent, student_manager):
        win = tk.Toplevel(parent)
        configure_window(win, "所有學生")

        student_listbox = tk.Listbox(win, width=40)
        student_listbox.pack()

        students = student_manager.load_students()
        for record in students:
            account = record[0]
            name = record[1] if len(record) > 1 else ""
            student_listbox.insert(tk.END, f"{account} ({name})")

        def on_select():
            selection = student_listbox.curselection()
            if not selection:
                messagebox.showerror("錯誤", "請先選擇一位學生")
                return

            selected_text = student_listbox.get(selection[0])
            account = selected_text.split(" ")[0]
            name = selected_text.split("(", 1)[1][:-1] if "(" in selected_text else account

            action = simpledialog.askstring(
                "操作選擇",
                f"對學生 {name} 執行何種操作？輸入：edit 或 delete"
            )
            if action == "edit":
                subject = simpledialog.askstring("科目", "請輸入科目：", parent=win)
                new_score = simpledialog.askinteger("分數", "請輸入新的分數：", parent=win)
                if subject and new_score is not None:
                    success = grade_manager.update_grade(username, account, subject, new_score)
                    if success:
                        messagebox.showinfo("成功", f"{name} 的 {subject} 成績已更新")
                    else:
                        messagebox.showerror("失敗", "未找到對應成績")
            elif action == "delete":
                subject = simpledialog.askstring("科目", "請輸入要刪除的科目：", parent=win)
                if subject:
                    confirm = messagebox.askyesno("確認刪除", f"確定刪除 {name} 的 {subject} 成績？")
                    if confirm:
                        success = grade_manager.delete_grade(username, account, subject)
                        if success:
                            messagebox.showinfo("成功", f"{name} 的 {subject} 成績已刪除")
                        else:
                            messagebox.showerror("失敗", "未找到對應成績")
            else:
                messagebox.showwarning("取消", "未執行任何操作")
        tk.Button(win, text="編輯／刪除選取學生成績", command=on_select).pack(pady=5)    
    tk.Button(dash, text="編輯／刪除學生成績", command=lambda: show_students_list(dash, student_manager)).pack(pady=3)

    def add_grade():
        student_account = simpledialog.askstring("學生帳號", "請輸入學生帳號：", parent=dash)
        subject = simpledialog.askstring("科目", "請輸入科目：", parent=dash)
        score = simpledialog.askinteger("分數", "請輸入分數：", parent=dash)
        if student_account and subject and score is not None:
            grade_manager.save_grade(username, student_account, subject, score)
            messagebox.showinfo("成功", "成績已新增")

    tk.Button(dash, text="新增學生成績", command=add_grade).pack(pady=3)

    def view_my_grades():
        grade_window = tk.Toplevel(dash)
        configure_window(grade_window, "已輸入的成績")
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
    configure_window(dash, "學生後台")

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
        configure_window(grade_window, "成績查詢")
        tk.Label(grade_window, text=f"{username} 的成績如下：").pack()
        listbox = tk.Listbox(grade_window, width=50)
        listbox.pack()
        for t, s, subj, score in grade_manager.load_grades():
            if s == account:
                listbox.insert(tk.END, f"{t} - {subj}: {score} 分")

    tk.Button(dash, text="查看個人資料", command=view_personal_info).pack(pady=3)
    tk.Button(dash, text="查看成績", command=view_grades).pack(pady=3)
    tk.Button(dash, text="關閉", command=dash.destroy).pack(pady=5)

# 主介面
def show_main_window():
    root = tk.Tk()
    configure_window(root, "登入系統")

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
