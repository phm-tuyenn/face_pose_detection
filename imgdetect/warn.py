import ctypes, threading
from pynput.keyboard import Key, Controller
import time, os, sys, time, json
from playsound import playsound

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Warn:
    warnThread = threading.Thread()

    def writeLog(self, message):
        filename = os.path.join("C:", "Users", "Public", "detect_log.json")
        try:
            open(filename, "r").close()
        except:
            open(filename, "w").write("[]")
        with open(filename, 'r', encoding="utf-8") as original:
            data = json.loads(original.read())
            original.close()
        with open(filename, 'w', encoding="utf-8") as modified:
            new = [{"timestamp": int(time.time() * 1000), "noti": message}]
            modified.write(json.dumps(new + data, ensure_ascii=False))
            modified.close()

    def showMessage(self, message):
        self.warnThread = threading.Thread(target = lambda : ctypes.windll.user32.MessageBoxW(None, message, "Hệ thống giám sát", 0X40 | 0x1000))
        self.warnThread.start()
        self.writeLog(message)

    def showOpeningMessage(self, code):
        threading.Thread(target = lambda : ctypes.windll.user32.MessageBoxW(None, "Chuơng trình giám sát đã được bắt đầu. Mã giám sát của bạn là " + code + ".", "Hệ thống giám sát", 0X40 | 0x1000)).start()
        self.writeLog("Chuơng trình giám sát được bắt đầu\n")

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
        playsound("./alarm.mp3")