from tkinter import *
import utils, json, changepw

top = Tk()
top.title("Cài đặt")

notify = StringVar()
notify.set("")

check_var = BooleanVar()

data = {}

def changepassword(_data, filename):
    global data
    if changepw.show(_data, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.loads(f.read()) 

def save(data, filename, detectTime, alarmTime, textLine):
    data["detectTime"] = int(detectTime)
    data["alarmTime"] = int(alarmTime)
    data["text"] = textLine
    data["runAtStartup"] = check_var.get()
    f = open(filename, "w")
    f.write(json.dumps(data))
    f.close()
    notify.set("Cài đặt đã được lưu lại!")

def show(_data, filename):
    data = _data
    Button(top, text="Đổi mật khẩu", command=lambda: changepassword(data, filename)).grid(row=0, column=0, columnspan=2)
    
    Label(top, text="Thời gian nhận diện (giây):").grid(row=1, column=0)
    Label(top, text="Thời gian báo hiệu âm thanh (giấy):").grid(row=2, column=0)
    Label(top, text="Lời nhắc:").grid(row=3, column=0)
    Label(top, text="Khởi chạy cùng Windows:").grid(row=4, column=0)

    detectTime = Entry(top)
    detectTime.insert(0, str(data["detectTime"]))
    detectTime.grid(row=1, column=1)
    alarmTime = Entry(top)
    alarmTime.insert(0, str(data["alarmTime"]))
    alarmTime.grid(row=2, column=1)
    textLine = Entry(top)
    textLine.insert(0, str(data["text"]))
    textLine.grid(row=3, column=1)

    startup = Checkbutton(top, variable=check_var)
    if data["runAtStartup"]:
        startup.select()
    else:
        startup.deselect()
    startup.grid(row=4, column=1)

    Button(top, text="Lưu thông tin", command=lambda: save(data, filename, detectTime.get(), alarmTime.get(), textLine.get())).grid(row=5, column=0, columnspan=2)
    Label(top, textvariable=notify, fg="green").grid(row=6, column=0, columnspan=2)
    
    utils.center(top)
    utils.focus(top)
    top.mainloop()