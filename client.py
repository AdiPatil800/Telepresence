import socket
import sys
import time
from naoqi import ALProxy
import json
import almath

host = "127.0.0.2"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 9686))

robotIP = "127.0.0.1"

PORT = 9559

motionProxy = ALProxy("ALMotion", robotIP, PORT)
motionProxy.setStiffnesses("LArm", 1.0)


# Example simulating reactive control
while True:
    
    
    msg = s.recv(1024)
    print(msg.decode())
    angleelbow = float(msg.decode())
    names = "LElbowRoll"
    angles = angleelbow*almath.TO_RAD
    #print(angles)
    fractionMaxSpeed = 1.0
    motionProxy.setAngles(names, -1*angles, fractionMaxSpeed)
    # wait half a second
    time.sleep(0.3)

# if __name__ == "__main__":
#     robotIp = "127.0.0.1"

#     if len(sys.argv) <= 1:
#         print( "Usage python almotion_reactivecontrol.py robotIP (optional default: 127.0.0.1)")
#     else:
#         robotIp = sys.argv[1]
