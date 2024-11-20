import cv2
import numpy as np
from pose_detection_mtcnn import *
import pandas as pd
from constant import *
from kalman import Kalman

kfRoll = Kalman(RollKalman.Q, RollKalman.R, RollKalman.N)
kfPitch = Kalman(PitchKalman.Q, PitchKalman.R, PitchKalman.N)
kfYaw = Kalman(YawKalman.Q, YawKalman.R, YawKalman.N)

# Recordings on/off
image_save = False
video_save = False
fps = 10.
video_format=cv2.VideoWriter_fourcc('M','J','P','G')
#video_max_frame=60
#video_outs=[]

# video capture initialization
camera = 0#0: internal, 1: external
cap = cv2.VideoCapture(camera)

res_actual = np.zeros((1,2), dtype=int)# initialize resolution
res_actual[0,0]=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
res_actual[0,1]=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print("camera resolution: {}".format(res_actual))

if video_save:
    video_file = 'video_out.avi'
    video_out = cv2.VideoWriter(video_file, video_format, fps, (640, 480))

data = []
processed_data = []

# process each frame from camera
while (True): 
    
    rets, frame = cap.read()
    if not (rets):
        print("Error: can't read from camera.")
        break
    
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)# convert to rgb
    image_rgb = cv2.flip(image_rgb, 1)# flip for user friendliness
    
    # face detection
    try:
        #bounding_boxes, landmarks = detector.detect_faces(image_rgb)
        bounding_boxes, landmarks = detect_faces(image_rgb)
        bbs = bounding_boxes.copy()
        lmarks = landmarks.copy()
    except:
        print("Error: face detector error.")
        break
    
    # if at least one face is detected
    if len(bounding_boxes) > 0:
        
        # process only one face (center ?) if multiple faces detected 
        #bb, lmarks_5 = one_face(image_rgb, bbs, lmarks)
        _, lmarks_5 = one_face(image_rgb, bbs, lmarks)
        #draw_landmarks(image_rgb, bb, lmarks_5)# draw landmarks and bbox 
        #
        #cv2.putText(image_rgb, "Face Pose", (10, 40), font, 0.8, blue, 2) 
        #cv2.putText(image_rgb, "Method 1", (10, 60), font, font_size, blue, 2) 
        #cv2.putText(image_rgb, "Roll: {0:.2f} (-50 to +50)".format(find_roll(lmarks_5)), (10, 80), font, font_size, blue, 1)  
        #cv2.putText(image_rgb, "Yaw: {0:.2f} (-100 to +100)".format(find_yaw(lmarks_5)), (10, 100), font, font_size, blue, 1)
        #cv2.putText(image_rgb, "Pitch: {0:.2f} (0 to 4)".format(find_pitch(lmarks_5)), (10, 120), font, font_size, blue, 1)
        
        angle, Xfrontal, Yfrontal = find_pose(lmarks_5)

        cv2.putText(image_rgb, "Raw", (10, 60), font, font_size, blue, 2)
        cv2.putText(image_rgb, "Roll: {0:.2f} degrees".format(angle), (10,80), font, font_size, blue, 1)
        cv2.putText(image_rgb, "Yaw: {0:.2f} degrees".format(Xfrontal), (10,100), font, font_size, blue, 1)
        cv2.putText(image_rgb, "Pitch: {0:.2f} degrees".format(Yfrontal), (10,120), font, font_size, blue, 1)

        processed_angle = kfRoll.estimate(angle)
        processed_Xfrontal = kfRoll.estimate(Xfrontal)
        processed_Yfrontal = kfRoll.estimate(Yfrontal)

        cv2.putText(image_rgb, "Processed", (10, 180), font, font_size, blue, 2)
        cv2.putText(image_rgb, "Roll: {0:.2f} degrees".format(processed_angle), (10,200), font, font_size, blue, 1)
        cv2.putText(image_rgb, "Yaw: {0:.2f} degrees".format(processed_Xfrontal), (10,220), font, font_size, blue, 1)
        cv2.putText(image_rgb, "Pitch: {0:.2f} degrees".format(processed_Yfrontal), (10,240), font, font_size, blue, 1)

        data.append([angle, Yfrontal, Xfrontal])
        processed_data.append([processed_angle, processed_Yfrontal, processed_Xfrontal])
        
        # smile detection
        #smile_ratio = find_smile(lmarks_5) 
        #if smile_ratio > 0.9:
        #    cv2.putText(image_rgb, "Smile: Yes", (10,280), font, font_size, blue, 2)
        #else:
        #    cv2.putText(image_rgb, "Smile: No", (10,280), font, font_size, blue, 2)
    else:
        cv2.putText(image_rgb, 'no face detected', (10, 20), font, font_size, blue, 2)
    
    if video_save:
        frame = cv2.resize(frame, (640, 480))
        video_out.write(frame)
    
    cv2.putText(image_rgb, "Press Q to quit.", (10, 460), font, font_size, blue, 1)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow('Face Pose Detection - MTCNN', image_bgr) 
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break
    
cap.release()

if video_save:
    video_out.release()

cv2.destroyAllWindows()

pd.DataFrame(data, columns=["roll", "pitch", "yaw"]).to_csv("output.csv", encoding='utf-8', index=False)
pd.DataFrame(processed_data, columns=["roll", "pitch", "yaw"]).to_csv("processed_output.csv", encoding='utf-8', index=False)