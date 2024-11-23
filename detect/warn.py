import ctypes, threading
from pynput.keyboard import Key, Controller
import time, os, sys
from playsound import playsound

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Warn:
    warnThread = threading.Thread()
    ranThread = threading.Thread(target = lambda : ctypes.windll.user32.MessageBoxW(None, "Chuơng trình giám sát đã được bắt đầu", "Hệ thống giám sát", 0X40 | 0x1000))

    def showMessage(self, message):
        self.warnThread = threading.Thread(target = lambda : ctypes.windll.user32.MessageBoxW(None, message, "Hệ thống giám sát", 0X40 | 0x1000))
        self.warnThread.start()

    def showOpeningMessage(self):
        self.ranThread.start()

    def isMessageOpen(self):
        return self.warnThread.is_alive()

    def setMaxVol(self):
        keyboard = Controller()
        pause = 0.0001
        
        press_count = int(100/2)
        for _ in range(press_count):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            time.sleep(pause)

    def playAlarm(self):
        self.setMaxVol()
        playsound(resource_path("alarm.mp3"))