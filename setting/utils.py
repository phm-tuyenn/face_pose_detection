from tkinter import *

def center(win, offsetX=0, offsetY=0):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2 + offsetX
    y = win.winfo_screenheight() // 2 - win_height // 2 - 50 + offsetY # 50 for offset so it will line up with user eyes
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def handle_focus(event, window):
    if event.widget == window:
        window.focus_set()

def focus(window):
    window.lift()
    window.attributes("-topmost", True)
    window.bind("<FocusIn>", lambda e: handle_focus(e, window))
    hwnd = window.winfo_id()