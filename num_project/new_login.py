import tkinter
import tkinter.font
import tkinter.messagebox
import sqlite3
import os
import sys
import hashlib
from get_path import get_path  # 确保get_path模块正确导入

def login():
    window = tkinter.Tk()
    window.title('登录')
    window.resizable(False, False)
    window.geometry('200x240+500+500')
    window.iconbitmap(os.path.join(get_path(), 'logo.ico'))
    
    login_status = {'success': False, 'auto_login': 0}  # 用字典替代全局变量

    def on_window_close():
        nonlocal login_status
        login_status['success'] = False
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', on_window_close)

    my_font = tkinter.font.Font(family='Consolas', size=35, weight='bold')
    tkinter.Label(text='登录', font=my_font).place(x=0, y=0, width=150, height=40)

    # 邮箱输入
    tkinter.Label(text='管理员邮箱').place(x=0, y=40, width=60, height=40)
    entry_email = tkinter.Entry()
    entry_email.place(x=60, y=40, width=100, height=40)

    # 密码输入
    tkinter.Label(text='管理员密码').place(x=0, y=80, width=60, height=40)
    entry_pwd = tkinter.Entry(show='*')
    entry_pwd.place(x=60, y=80, width=100, height=40)

    # 自动登录选项
    auto_login_var = tkinter.IntVar(value=1)
    tkinter.Checkbutton(text='下次自动登录', variable=auto_login_var,
                        onvalue=1, offvalue=0).place(x=20, y=120, width=100, height=25)

    def check_credentials():
        email = entry_email.get()
        pwd = entry_pwd.get()
        
        # 数据库操作
        if not os.path.exists(r'D:\AppData'):
            os.makedirs(r'D:\AppData')
        
        conn = sqlite3.connect(r'D:\AppData\data.db')
        try:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS ADMIN(email TEXT, password TEXT)')
            
            # 检查是否存在初始数据
            cursor.execute('SELECT COUNT(*) FROM ADMIN')
            if cursor.fetchone()[0] == 0:
                default_email = hashlib.sha256('ZSCinYBSZ2023@outlook.com'.encode()).hexdigest()
                default_pwd = hashlib.sha256('3320230346with39'.encode()).hexdigest()
                cursor.execute('INSERT INTO ADMIN VALUES (?, ?)', (default_email, default_pwd))
                conn.commit()
            
            # 验证输入
            input_hash = (
                hashlib.sha256(email.encode()).hexdigest(),
                hashlib.sha256(pwd.encode()).hexdigest()
            )
            cursor.execute('SELECT * FROM ADMIN LIMIT 1')
            db_data = cursor.fetchone()
            
            if input_hash == db_data:
                login_status['success'] = True
                login_status['auto_login'] = auto_login_var.get()
                window.destroy()  # 验证成功后立即关闭窗口
                tkinter.messagebox.showinfo('登录成功', '恭喜！登录成功')
            else:
                tkinter.messagebox.showerror('失败', '邮箱或密码错误')
        finally:
            conn.close()

    tkinter.Button(text='提交', command=check_credentials).place(x=130, y=130, width=55, height=30)
    tkinter.Button(text='取消', command=sys.exit).place(x=130, y=190, width=55, height=30)
    
    window.mainloop()
    return login_status['auto_login'] if login_status['success'] else None


if __name__ == '__main__':
    result = login()
    print("登录状态:", "自动登录已启用" if result == 1 else ("自动登录未启用" if result == 0 else "登录取消"))
