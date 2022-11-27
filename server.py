import socket
import cv2
import mediapipe as mp
import numpy as np
import time


host="127.0.0.2"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, 9686))
s.listen(5)
clientsocket, address = s.accept()
print(f"connection from {address} has been established")
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


result = []


def cal_ang(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
        np.arctan2(b[1] - a[1], b[0] - a[0])
    ang = np.abs(radians * 180.0 / np.pi)

    if ang > 180:
        ang = 360 - ang

    return ang


cap = cv2.VideoCapture(0)

count = 0
stage = None
with mp_pose.Pose(min_detection_confidence=0.9, min_tracking_confidence=0.9) as pose:
    while cap.isOpened():
        ret, frm = cap.read()

        img = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False

        results = pose.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_world_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            angle = cal_ang(shoulder, elbow, wrist)
            print(str(angle))
            clientsocket.send(str(angle).encode())
            time.sleep(0.5)

        except:
            pass

        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Jai Shri Ram', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
