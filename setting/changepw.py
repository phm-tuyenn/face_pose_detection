from tkinter import *
from hashlib import sha256
import bcrypt, utils, json

safeExit = False

def change(top, data, filename, code, password, newpw, notify):
    global safeExit
    if (code == data["code"]) and (bcrypt.checkpw(sha256(password.encode("utf8")).hexdigest().encode("utf8"), data["password"].encode("utf8"))):
        data["password"] = bcrypt.hashpw(sha256(newpw.encode("utf8")).hexdigest().encode("utf8"), bcrypt.gensalt()).decode("utf8")
        f = open(filename, "w")
        f.write(json.dumps(data))
        f.close()
        safeExit = True
        top.destroy()
    else:
        notify.set("Sai thông tin đăng nhập. Hãy thử lại!")

def show(data, filename):
    top = Tk()
    top.title("Đổi mật khẩu")

    notify = StringVar()
    notify.set("")

    Label(top, text="Mã giám sát:").grid(row=0, column=0)
    Label(top, text="Mật khẩu của phụ huynh:").grid(row=1, column=0)
    Label(top, text="Mật khẩu mới:").grid(row=2, column=0)

    code = Entry(top)
    code.insert(0, data["code"])
    code.grid(row=0, column=1)
    password = Entry(top, show="*")
    password.grid(row=1, column=1)
    newpassword = Entry(top, show="*")
    newpassword.grid(row=2, column=1)

    Button(top, text="Đổi mật khẩu", command=lambda: change(top, data, filename, code.get(), password.get(), newpassword.get(), notify)).grid(row=3, column=1)
    Label(top, textvariable=notify, fg="red").grid(row=4, column=0, columnspan=2)

    utils.center(top, offsetY=100)
    utils.focus(top)
    top.mainloop()

    return safeExit