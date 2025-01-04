import cv2, time, json, os, threading, checkTrig
from random import randrange
import numpy as np
from pose_detection_mtcnn import *
import constant as const
from kalman import Kalman
from warn import Warn

#init warning windows
warn = Warn()

#init kalman filter
kfRoll = Kalman(const.RollKalman.Q, const.RollKalman.R, const.RollKalman.N)
kfPitch = Kalman(const.PitchKalman.Q, const.PitchKalman.R, const.PitchKalman.N)
kfYaw = Kalman(const.YawKalman.Q, const.YawKalman.R, const.YawKalman.N)

# video capture initialization
camera = 0#0: internal, 1: external
cap = cv2.VideoCapture(camera)

res_actual = np.zeros((1,2), dtype=int)# initialize resolution
res_actual[0,0]=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
res_actual[0,1]=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print("camera resolution: {}".format(res_actual))

time_detect = -1
time_stamp = -1

openPath = os.path.join("C:", "Users", "Public", "open.json")
if not os.path.exists(openPath):
    f = open(openPath, "w")
    f.write(json.dumps({
        "open": False
    }))
    f.close()

filename = os.path.join("C:", "Users", "Public", "setting.json")
data = json.loads(open(filename, "r", encoding="utf8").read())
if not os.path.exists(filename):
    f = open(filename, "w")
    f.write(json.dumps({
        "code": str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + str(randrange(10)),
        "password": "$2b$12$zoHuqo7EpPxE0bTNOTh6LOlvjuJFdgaE/dpUl0.2RemQkdlSoto4u",
        "detectTime": 2,
        "alarmTime": 120
    }))
    f.close()

def getOpenTrigger():
    try:
        return json.loads(open(openPath, "r", encoding="utf8").read())["open"]
    except:
        return False
    
threading.Thread(target=checkTrig.loop).start()

while True:
    print("app ok")
    # wait for a trigger from outside
    # TODO: do a trigger from http server in localhost
    while not getOpenTrigger(): pass

    warn.showOpeningMessage(data["code"])

    while getOpenTrigger():
        rets, frame = cap.read()
        if not (rets):
            warn.showMessage("Hệ thống không nhận được dữ liệu từ camera của bạn! Vui lòng khởi động lại máy tính!")
            break
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)# convert to rgb
        image_rgb = cv2.flip(image_rgb, 1)# flip for user friendliness
        
        # face detection
        try:
            bounding_boxes, landmarks = detect_faces(image_rgb)
            bbs = bounding_boxes.copy()
            lmarks = landmarks.copy()
        except:
            warn.showMessage("Hệ thống đang bị lỗi nhận dạng! Vui lòng khởi động lại máy tính!")
            break
        
        # if at least one face is detected
        if len(bounding_boxes) > 0:
            # process only one face (center ?) if multiple faces detected 
            _, lmarks_5 = one_face(image_rgb, bbs, lmarks)
            
            _, Xfrontal, Yfrontal = find_pose(lmarks_5)
            # processed_angle = kfRoll.estimate(angle)
            processed_Xfrontal = kfYaw.estimate(Xfrontal)
            processed_Yfrontal = kfPitch.estimate(Yfrontal)

            print(processed_Xfrontal, processed_Yfrontal, time_detect)

            if (abs(processed_Xfrontal) > 50 or abs(processed_Yfrontal) > 50):
                if time_detect == -1: 
                    time_detect = time.time()
            else:
                time_detect = -1

        elif time_detect == -1:
            time_detect = time.time()

        if (time_detect != -1 and (time.time() - time_detect) >= data["detectTime"]):
            print("hey")
            if not warn.isMessageOpen():
                warn.showMessage("Bạn đang không hướng mặt vào màn hình!")
                time_stamp = time.time()
            time_detect = -1
        
        if time_stamp != -1 and (time.time() - time_stamp) >= data["alarmTime"] and warn.isMessageOpen():
            warn.playAlarm()
            time_stamp = time.time()