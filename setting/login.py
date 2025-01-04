from tkinter import *
from hashlib import sha256
import bcrypt, utils

top = Tk()
top.title("Đăng nhập")

notify = StringVar()
notify.set("")

safeExit = False

def login(data, code, password):
    global safeExit
    if (code == data["code"]) and (bcrypt.checkpw(sha256(password.encode("utf8")).hexdigest().encode("utf8"), data["password"].encode("utf8"))):
        safeExit = True
        top.destroy()
    else:
        notify.set("Sai thông tin đăng nhập. Hãy thử lại!")

def show(data):
    Label(top, text="Mã giám sát:").grid(row=0, column=0)
    Label(top, text="Mật khẩu của phụ huynh:").grid(row=1, column=0)

    code = Entry(top)
    code.insert(0, data["code"])
    code.grid(row=0, column=1)
    password = Entry(top, show="*")
    password.grid(row=1, column=1)

    Button(top, text="Đăng nhập", command=lambda: login(data, code.get(), password.get())).grid(row=2, column=1)
    Label(top, textvariable=notify, fg="red").grid(row=3, column=0, columnspan=2)

    utils.center(top)
    utils.focus(top)
    top.mainloop()

    return safeExit