# -*- coding: gbk -*-
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
from time import time
import threading
import mythread
import urlwork
import time
from _datetime import datetime
import inspect
import ctypes
from threading import Thread

urlwork = urlwork.MyUrl()
event_flag = threading.Event()

thList = []


def getCurrentTime():  # 获取系统当前时间
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def insertScr(str):  # 在tab1中的scr中输出工作记录
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " " + str)
    scr.see(tk.END)


def loginbtn():  # tab登录按钮
    insertScr("\n用户名:" + uname.get() + '\n密码:' + pwd.get() + "\n邀请码:" + inv.get())
    token = urlwork.getToken(uname.get(), pwd.get())
    if (token.decode("gbk") != "-2"):
        try:
            with open("account") as fp:
                tkinter.messagebox.showinfo(title='恭喜', message='登录成功！')
                # 把登录成功的信息写入临时文件
                with open(filename, 'w') as fp:
                    fp.write(','.join((uname.get(), pwd.get())))
        except:
            pass
        insertScr("登录成功")

        # tkinter.messagebox.showinfo(title="提示", message="登录成功")
    else:
        insertScr("登录失败")
        # tkinter.messagebox.showinfo(title="提示", message="登录失败")


def radiobuttonDo():  # tab1单选按钮
    insertScr("你点击了radiobutton " + var.get())
    if (var.get() == "d"):
        scr.delete(1.0, tkinter.END)


# 杀死线程
def stopTh(tid, msg, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    insertScr(msg + "已结束工作!")


def doWork(msg):
    insertScr(msg+"开始工作...")
    # 1.获取token    if (loginbtn):
    logintoken = urlwork.getToken(uname.get(), pwd.get())
    # 2.获取手机号

    while 3:
        telNumber = urlwork.getTelNum(logintoken)
        insertScr(msg + "手机号:" + telNumber[3:13].decode("gbk"))
        # 3.获取验证码
        verification_code = ""
        for i in range(100):
            verification_code = urlwork.getVerificationCode(logintoken, telNumber)
            if (verification_code.decode("gbk") != "-1"):
                insertScr(msg + "验证码:" + verification_code.decode("gbk"))
                break
            else:
                insertScr(msg + "获取验证码失败  " + verification_code.decode("gbk"))
                time.sleep(6)
    # 4.释放手机号
    n = urlwork.releaseNum(logintoken, telNumber[3:13])
    if (n.decode("gbk") == "1"):
        insertScr(msg + "号码释放成功")
    else:
        insertScr(msg + "号码释放失败")


def creatTh(maxNum):
    global thList
    thList=[]
    for i in range(maxNum):
        i = threading.Thread(target=doWork, name=str(i), args=("[程序" + str(i) + "]",))
        thList.append(i)
    return thList


def runbtn():
    th = creatTh(thtext.get())
    for t in th:
        # t.setDaemon(True)
        t.start()


def stopbtn():
    for th in thList:
        stopTh(th.ident, "[程序" + th.getName() + "]", SystemExit)


def checkEntry():
    if (uname.get().replace(" ", "") == ""):
        tkinter.messagebox.showwarning("警告", "用户名不能为空!")


def checkThEntry(content):
    def test(content):
        # 如果不加上==""的话，就会发现删不完。总会剩下一个数字
        if content.isdigit() or content == "":
            return True
        else:
            tkinter.messagebox.showwarning("警告", "线程必须是数字!")
            return False


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
thentrycheck = root.register(checkThEntry)
nameandpwdentrycheck = root.register(checkEntry)
style.configure("BW.TLabel", foreground="#32CD32", background="white")

var = tk.StringVar()

label_frame_log = ttk.LabelFrame(tab1, text="运行记录", width=400, height=400)
controlled_center_frame = ttk.LabelFrame(tab1, text="控制中心", width=400, height=280)
controlled_center_bottom_frame = ttk.LabelFrame(controlled_center_frame, text="操作区", width=390, height=300)
controller_center_head_frame = ttk.LabelFrame(controlled_center_frame, text="短信", width=390, height=300)

controller_center_head_frame.grid(row=0, padx=5, sticky=tk.N + tk.W + tk.E)
controlled_center_frame.grid(row=0, column=1, padx=5, sticky=tk.N)
label_frame_log.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S)
controlled_center_bottom_frame.grid(row=1, padx=5)
radiobutton1 = ttk.Radiobutton(controller_center_head_frame, text="讯码", variable=var, value="a", command=radiobuttonDo)
radiobutton2 = ttk.Radiobutton(controller_center_head_frame, text="众码", variable=var, value="d", command=radiobuttonDo)
radiobutton3 = ttk.Radiobutton(controller_center_head_frame, text="快码", variable=var, value="c", command=radiobuttonDo)
# radiobutton4 = ttk.Radiobutton(controller_center_head_frame , text="神话", variable=var, value="c", command=radiobuttonDo)
user_name = ttk.Label(controller_center_head_frame, text="用户名:")
password = ttk.Label(controller_center_head_frame, text="密   码:")
Invite_code = ttk.Label(controlled_center_bottom_frame, text="邀请码:")
loginbtn = tk.Button(controller_center_head_frame, text="登录", command=loginbtn)

thlabel = ttk.Label(controlled_center_bottom_frame, text="线程数:")
ctrlabel = ttk.Label(controlled_center_bottom_frame, text="操作数:")
iplabel = ttk.Label(controlled_center_bottom_frame, text="IP频率:")
diallabel = ttk.Label(controlled_center_bottom_frame, text="拨号延迟:")
randomcheck= ttk.Checkbutton(controlled_center_bottom_frame, text="随机密码")
fixedpwdlab = ttk.Label(controlled_center_bottom_frame, text="固定密码:")

runbutton = tk.Button(controlled_center_bottom_frame, text="运行", command=runbtn, width=10)
stopbutton = tk.Button(controlled_center_bottom_frame, text="停止", command=stopbtn, width=10)
scr = scrolledtext.ScrolledText(label_frame_log, width=50, height=80)
scr.grid(row=0, column=0, pady=0)
uname = tk.StringVar()
uname_text = ttk.Entry(controller_center_head_frame, textvariable=uname, validate='focusout',
                       validatecommand=(nameandpwdentrycheck, '%P'))
pwd = tk.StringVar()
pwd_text = ttk.Entry(controller_center_head_frame, textvariable=pwd, validatecommand=(nameandpwdentrycheck, '%P'))
inv = tk.StringVar()
inv_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=inv)
thtext = tk.IntVar()
thtext.set(1)
th_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=thtext, validate='key',
                    validatecommand=(thentrycheck, '%P'))
ctrtext = tk.IntVar()
ctrtext.set(1)
ctr_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=ctrtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
iptext = tk.IntVar()
iptext.set(1)
ip_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=iptext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
dialtext = tk.IntVar()
dialtext.set(1)
dial_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=dialtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
fixedpwd = tk.IntVar()
fixedpwd.set(1)
fixedpwd_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=fixedpwd, validate='key',
                     validatecommand=(thentrycheck, '%P'))
radiobutton1.grid(row=0, column=0, padx=5)
radiobutton2.grid(row=0, column=1, padx=5)
radiobutton3.grid(row=0, column=2, padx=5)
# radiobutton4.grid(row=0,column=3,padx=5,sticky=tk.E)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)

thlabel.grid(row=0, column=2, padx=2, pady=3)
th_text.grid(row=0, column=3, padx=2, pady=3)
ctrlabel.grid(row=0, column=0, padx=2, pady=3)
ctr_text.grid(row=0, column=1, padx=2, pady=3)
iplabel.grid(row=1,column=0,padx=2,pady=3)
ip_text.grid(row=1,column=1,padx=2,pady=3)
diallabel.grid(row=1,column=2,padx=2,pady=3)
randomcheck.grid(row=2,column=0,padx=2,pady=3)
fixedpwdlab.grid(row=2,column=2,padx=5,pady=3)
fixedpwd_text.grid(row=2,column=3,padx=2,pady=3)
dial_text.grid(row=1,column=3,padx=2,pady=3)
Invite_code.grid(row=4, column=0,padx=2, pady=3)
inv_text.grid(row=4, column=1, padx=2, pady=3)

loginbtn.grid(row=5, ipadx=20, padx=2, pady=3)

runbutton.grid(row=6, column=0, padx=5, sticky=tk.S)
stopbutton.grid(row=6, column=1, padx=5, sticky=tk.S + tk.E)
try:
    with open("account") as fp:
        n, p = fp.read().strip().split(',')
        uname.set(n)
        pwd.set(p)
except:
    pass

root.mainloop()
