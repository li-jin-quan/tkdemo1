# -*- coding: gbk -*-
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
from time import time
import urllib.parse
import urllib.request
import  threading
import mythread

import time
from _datetime import datetime


class WinApp(object):
    def __init__(self):
        a = 1


def getCurrentTime():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def loginbtn():
    scr.insert(tk.INSERT,
               getCurrentTime() + "\n" + "用户名:" + uname.get() + '\n' + "密码:" + pwd.get() + "\n" + "邀请码:" + inv.get() + "\n")
    token = getToken()
    if (token != -2):
        scr.insert(tk.INSERT, getCurrentTime() + " \n登录成功 token:" + token.decode("gbk"))
        # tkinter.messagebox.showinfo(title="提示", message="登录成功")
    else:
        scr.insert(tk.INSERT, getCurrentTime() + "登录失败" + token.decode("gbk"))
        # tkinter.messagebox.showinfo(title="提示", message="登录失败")
    return token


def getResponse(url, data):
    params = urllib.parse.urlencode(data)
    url = url % params
    with urllib.request.urlopen(url, timeout=100) as response:
        return response.read()


def getTelNum(token):
    data = {
        "token": token,
        "xmid": 200,
        "sl": 1,
        "lx": 1,
        "a1": "",
        "a2": "",
        "pk": "",
        "ks": 0,
        "rj": 0
    }
    url = 'http://47.106.71.60:9180/service.asmx/GetHM2Str?%s'
    return getResponse(url, data)


def getVerificationCode(token, telNumber):
    url = "http://47.106.71.60:9180/service.asmx/GetYzm2Str?%s"
    data = {
        "token": token,
        "hm": telNumber[3:13],
        "xmid": 200,
        "sf": 0
    }
    return getResponse(url, data)


def getToken():
    data = {
        "name": uname.get(),
        "psw": pwd.get()
    }
    url = "http://47.106.71.60:9180/service.asmx/UserLoginStr?%s"
    return getResponse(url, data)


def radiobuttonDo():
    scr.insert(tk.INSERT, "\n" + " 你点击了radiobutton    " + var.get())
    if (var.get() == "d"):
        scr.delete(1.0, tkinter.END)


def doWork(msg):
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + msg)
    stopbutton["background"] = "#F5F5F5"  # 白灰
    runbutton["background"] = "SpringGreen"  # 闪光绿
    # 1.获取token    if (loginbtn):
    logintoken = getToken()
    # 2.获取手机号
    telNumber = getTelNum(logintoken)
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " 手机号:" + telNumber[3:13].decode("gbk"))
    # 3.获取验证码
    while 1:
        verification_code = getVerificationCode(logintoken, telNumber)
        if (verification_code.decode("gbk") != "-1"):
            scr.insert(tk.INSERT, "\n" + getCurrentTime() + " 验证码:" + verification_code.decode("gbk"))
            break
        else:
            scr.insert(tk.INSERT, "\n" + getCurrentTime() + " 获取验证码失败  " + verification_code.decode("gbk"))
            time.sleep(6)

    # 4.释放手机号


def runbtn():
    runbutton["background"] = "#008000"  # 纯绿
    stopbutton["background"] = "#F5F5F5"  # 番茄红
    th = threading.Thread(target=doWork, args=("\n" + " 开始工作.....",))
    th.setDaemon(True)  # 守护线程
    th.start()
    # th = mythread.Th(target=doWork, args=("\n" + " 开始工作.....",))
    # th.setDaemon(True)  # 守护线程
    # th.start()


def stopbtn():
    runbutton["background"] = "#F5F5F5"  # 白灰
    stopbutton["background"] = "#FF6347"  # 番茄红


def checkEntry():
    if (uname.get().replace(" ", "") == ""):
        tkinter.messagebox.showwarning("警告", "用户名不能为空!")



root = tk.Tk()
root.title("飞蚁")
root.geometry('810x660')  # 是x 不是*
root.resizable(width=False, height=0)  # 宽不可变, 高不可变,默认为0
tabControl = ttk.Notebook(root, height=620, padding=0, width=800, style="BW.TLabel")
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text=" 工作台 ")
tabControl.add(tab2, text=" 设  置 ")
tabControl.add(tab3, text=" 账  号 ")
tabControl.grid(padx=4, pady=4)

style = ttk.Style()

style.configure("BW.TLabel", foreground="#32CD32", background="white")

var = tk.StringVar()

label_frame_loging = ttk.LabelFrame(tab1, text="登录区", width=300, height=300)
label_frame_log = ttk.LabelFrame(tab1, text="运行记录", width=400, height=500)
label_frame_loging.grid(row=0, column=1, padx=5, sticky=tk.N)
label_frame_log.grid(row=0, column=0, padx=5, sticky=tk.S)

radiobutton1 = ttk.Radiobutton(label_frame_loging, text="讯码", variable=var, value="a", command=radiobuttonDo)
radiobutton2 = ttk.Radiobutton(label_frame_loging, text="众码", variable=var, value="d", command=radiobuttonDo)
user_name = ttk.Label(label_frame_loging, text="用户名:")
password = ttk.Label(label_frame_loging, text="密码:")
Invite_code = ttk.Label(label_frame_loging, text="邀请码:")
loginbtn = tk.Button(label_frame_loging, text="登录", command=loginbtn)
runbutton = tk.Button(tab1, text="运行", command=runbtn, width=10)
stopbutton = tk.Button(tab1, text="停止", command=stopbtn, width=10)
scr = scrolledtext.ScrolledText(label_frame_log, width=50)
scr.grid(row=0, column=0, pady=0)
uname = tk.StringVar()
uname_text = ttk.Entry(label_frame_loging, textvariable=uname, validate='focusout', validatecommand=checkEntry)
pwd = tk.StringVar()
pwd_text = ttk.Entry(label_frame_loging, textvariable=pwd)
inv = tk.StringVar()
inv_text = ttk.Entry(label_frame_loging, textvariable=inv)
radiobutton1.grid(row=0, column=0)
radiobutton2.grid(row=0, column=1)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)
Invite_code.grid(row=3, padx=2, pady=3)
inv_text.grid(row=3, column=1, padx=2, pady=3)
loginbtn.grid(row=4, ipadx=20)

runbutton.grid(row=0, column=1, padx=5, sticky=tk.S)
stopbutton.grid(row=0, column=1, padx=5, sticky=tk.S + tk.E)

root.mainloop()
