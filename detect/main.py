import cv2, time
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

delay_count = 0
time_stamp = -1

warn.showOpeningMessage()

while (True):     
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
        
        angle, Xfrontal, Yfrontal = find_pose(lmarks_5)
        # processed_angle = kfRoll.estimate(angle)
        processed_Xfrontal = kfYaw.estimate(Xfrontal)
        processed_Yfrontal = kfPitch.estimate(Yfrontal)

        print(processed_Xfrontal, processed_Yfrontal)

        if abs(processed_Xfrontal) > 50 or abs(processed_Yfrontal) > 50:
            delay_count += 1
        else:
            delay_count = 0

    else:
        delay_count += 1

    if delay_count >= const.DELAY_NUMBER:
        print("hey")
        if not warn.isMessageOpen():
            warn.showMessage("Bạn đang không hướng mặt vào màn hình!")
            time_stamp = time.time()
        delay_count = 0
    
    if time_stamp != -1 and (time.time() - time_stamp) >= 120 and warn.isMessageOpen():
        warn.playAlarm()
        time_stamp = time.time()
        
cap.release()
cv2.destroyAllWindows()