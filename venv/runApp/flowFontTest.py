from tkinter import *
import time
root = Tk()
root.title("Marquee")
root.geometry("320x240+100+100")
show_str = StringVar(root)
show_str.set("this")
source_str = "测试数据:这里是流动文字测试,颜色(红)"
stopflag = True
pos = 0
def marquee(widget):
   textwidth = 200
   strlen = len(source_str)
   global pos
   if strlen - pos < textwidth:
       show_str.set(source_str[pos:pos+textwidth] + source_str[0:textwidth - strlen + pos])
   else:
       show_str.set(source_str[pos:pos+textwidth])
   pos += 1
   if pos > strlen:
       pos = 0
   global stopflag
   if stopflag:
       widget.after(100, marquee, widget)
show_lb = Label(root,anchor=W ,textvariable=show_str)
show_lb.place(x=20, y=20, width=200, height=30)
def startmarque():
   global stopflag
   stopflag = True
   marquee(show_lb)
def stopmarquee():
   global stopflag
   stopflag = False
button1 = Button(root, text="start", command=startmarque)
button2 = Button(root, text="stop", command=stopmarquee)
button1.place(x=20, y=100, width=50, height=30)
button2.place(x=200, y=100, width=50, height=30)
root.mainloop()