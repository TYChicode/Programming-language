# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import base64
import os
from rsa_utils import *

DATA_FILE = "users.txt"
STUDENT_FILE = "students.txt"

# 載入或建立密鑰
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key)
else:
    private_key = load_private_key()
    public_key = load_public_key()

# 儲存帳號
def save_user(username, password):
    encrypted_user = encrypt_data(public_key, username)
    encrypted_pass = encrypt_data(public_key, password)
    with open(DATA_FILE, "ab") as f:
        f.write(base64.b64encode(encrypted_user) + b":" + base64.b64encode(encrypted_pass) + b"\n")

# 驗證帳號
def check_login(username, password):
    if not os.path.exists(DATA_FILE):
        return False
    with open(DATA_FILE, "rb") as f:
        for line in f:
            user_b64, pass_b64 = line.strip().split(b":")
            try:
                stored_user = decrypt_data(private_key, base64.b64decode(user_b64))
                stored_pass = decrypt_data(private_key, base64.b64decode(pass_b64))
                if stored_user == username and stored_pass == password:
                    return True
            except Exception:
                continue
    return False

# 儲存學生
def save_student(name, age):
    encrypted_name = encrypt_data(public_key, name)
    encrypted_age = encrypt_data(public_key, str(age))
    with open(STUDENT_FILE, "ab") as f:
        f.write(base64.b64encode(encrypted_name) + b":" + base64.b64encode(encrypted_age) + b"\n")

# 載入學生
def load_students():
    students = []
    if not os.path.exists(STUDENT_FILE):
        return students
    with open(STUDENT_FILE, "rb") as f:
        for line in f:
            name_b64, age_b64 = line.strip().split(b":")
            try:
                name = decrypt_data(private_key, base64.b64decode(name_b64))
                age = decrypt_data(private_key, base64.b64decode(age_b64))
                students.append((name, age))
            except Exception:
                continue
    return students

# 主功能頁面
def show_dashboard():
    dash = tk.Toplevel()
    dash.title("學生管理系統")

    tk.Label(dash, text="目前學生名單：").pack()

    student_listbox = tk.Listbox(dash, width=40)
    student_listbox.pack()

    def refresh_students():
        student_listbox.delete(0, tk.END)
        for name, age in load_students():
            student_listbox.insert(tk.END, f"{name} - {age} 歲")

    def add_student():
        name = simpledialog.askstring("輸入學生姓名", "請輸入姓名：", parent=dash)
        age = simpledialog.askinteger("輸入學生年齡", "請輸入年齡：", parent=dash)
        if name and age is not None:
            save_student(name, age)
            refresh_students()

    tk.Button(dash, text="新增學生", command=add_student).pack(pady=5)
    tk.Button(dash, text="重新整理", command=refresh_students).pack()

    refresh_students()

# 登入頁面
def show_main_window():
    root = tk.Tk()
    root.title("登入系統")

    def login():
        username = entry_user.get()
        password = entry_pass.get()
        if check_login(username, password):
            messagebox.showinfo("成功", "登入成功")
            root.destroy()
            show_dashboard()
        else:
            messagebox.showerror("失敗", "登入失敗")

    def register():
        username = entry_user.get()
        password = entry_pass.get()
        save_user(username, password)
        messagebox.showinfo("註冊成功", "帳號已註冊")

    tk.Label(root, text="帳號:").grid(row=0, column=0)
    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1)

    tk.Label(root, text="密碼:").grid(row=1, column=0)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.grid(row=1, column=1)

    tk.Button(root, text="登入", command=login).grid(row=2, column=0)
    tk.Button(root, text="註冊", command=register).grid(row=2, column=1)

    root.mainloop()

show_main_window()
