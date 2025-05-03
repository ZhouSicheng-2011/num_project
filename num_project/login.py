import tkinter
import tkinter.font
import tkinter.messagebox

import sqlite3
import os
import sys
import hashlib

#get path
import get_path

a=0
def login():
    global a
    #创建窗口
    window=tkinter.Tk()
    window.title('登录')
    window.resizable(False,False)
    window.geometry('200x180+500+500')
    window.iconbitmap(os.path.join(get_path.get_path(),'logo.ico'))
    #字体定义
    my_font=tkinter.font.Font(
        family='Consolas',
        size=35,
        weight='bold'
    )
    #配置标题
    label_0=tkinter.Label(text='登录',font=my_font)
    label_0.place(x=0,y=0,width=150,height=40)
    #登录信息
    label_1=tkinter.Label(text='管理员邮箱')
    label_1.place(x=0,y=40,width=60,height=40)

    entry_0=tkinter.Entry()
    entry_0.place(x=60,y=40,width=100,height=40)


    label_2=tkinter.Label(text='管理员密码')
    label_2.place(x=0,y=80,width=60,height=40)

    entry_1=tkinter.Entry()
    entry_1.place(x=60,y=80,width=100,height=40)
    #自动登录
    self_login=tkinter.IntVar(value=1)
    check_button_1=tkinter.Checkbutton(text='下次自动登录',variable=self_login,
    onvalue=1,offvalue=0)
    check_button_1.place(x=20,y=120,width=100,height=25)

    button=tkinter.Button(text='提交',command=lambda: check((entry_0.get(),
    entry_1.get())))
    button.place(x=130,y=130,width=55,height=30)
    #主循环
    window.mainloop()
    if a==1:
        l=self_login.get()
        #window.destroy()
        return l

def check(ipt:tuple):
    global a
    #数据查询
    if not os.path.exists(r'D:\AppData'):
        os.makedirs(r'D:\AppData')
    database=sqlite3.connect(r'D:\AppData\data.db')
    cur=database.cursor()
    try:
        r=cur.execute('select * from ADMIN')
        if not r.fetchone():
            raise IOError
        result=tuple(r.fetchone())
        del r
    except Exception:
        try:
            cur.execute('create table ADMIN(email text,password text)')
        except:
            pass
        cur.execute('insert into ADMIN(email,password) values(?,?)',
        tuple([hashlib.sha256('ZSCinYBSZ2023@outlook.com'.encode()).hexdigest(),
        hashlib.sha256('3320230346with39'.encode()).hexdigest()]))
        database.commit()
        r=cur.execute('select * from ADMIN')
        result=tuple(r.fetchone())

    #数据比对
    gets=tuple([hashlib.sha256(ipt[0].encode()).hexdigest(),
    hashlib.sha256(ipt[1].encode()).hexdigest()])

    if gets==result:
        tkinter.messagebox.showinfo(title='登录成功',message='恭喜！登录成功')
        a=1
    else:
        tkinter.messagebox.showerror(title='失败',message='登录失败!') 
        a=0
    database.close()

    

if __name__=='__main__':
    print(login())